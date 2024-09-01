from typing import Dict, Any, List, Union
from creao.core.Dedup import Dedup
import networkx as nx
import yaml
from networkx.algorithms.dag import topological_sort
from creao.core.Endpoints import OpenAILLM, CreaoLLM
import json
from pydantic import BaseModel, create_model
from datasets import load_dataset
from jinja2 import Template, Environment, meta
from tqdm import tqdm
from collections import defaultdict
from itertools import product
import os
import requests

def flatten_list(l):
  for item in l:
    if isinstance(item, list):
      yield from flatten_list(item)
    else:
      yield item


def list_of_dicts_to_dict_of_lists(res_list: List[Dict[str, str]]) -> Dict[str, List[str]]:
    # Initialize an empty dictionary to collect the lists
    result = {}
    # Check if the list is empty to avoid errors
    if not res_list:
        return result
    # Initialize the result dictionary with empty lists for each key
    for key in res_list[0]:
        result[key] = []
    # Populate the lists
    for item in res_list:
        for key in item:
            result[key].append(item[key])
    for key in result:
        result[key] = list(flatten_list(result[key]))
    return result

def convert_dict_list(dict_list):
    # Extract the keys and values from the list of dicts
    keys = []
    values = []
    for d in dict_list:
        for k, v in d.items():
            keys.append(k)
            values.append(v)
    
    # Generate Cartesian product of the values
    combinations = product(*values)
    
    # Construct new dictionaries from each combination
    result = [dict(zip(keys, combo)) for combo in combinations]
    
    return result

# Utility functions for schema validation
def validate_schema(data: Dict[str, Any], schema: Dict[str, type], instance_name: str, validation_type: str) -> None:
    for key, expected_type in schema.items():
        if key not in data:
            raise ValueError(f"Missing key '{key}' in {validation_type} for '{instance_name}'")
        if not isinstance(data[key], expected_type):
            raise TypeError(f"Key '{key}' in {validation_type} for '{instance_name}' expected to be of type {expected_type}, but got {type(data[key])}")

# Class registry for components
class_registry = {}

def creao_component(cls):
    """
    Registers the class and wraps its `run` method with input/output validation logic.
    """
    original_run_method = getattr(cls, "run", None)
    if original_run_method is None:
        raise ValueError(f"Class {cls.__name__} must have a 'run' method.")

    input_schema = getattr(cls, "input_schema", None)
    output_schema = getattr(cls, "output_schema", None)

    def wrapped_run(self, chained_input:List[Dict[str,List[str]]], *args, **kwargs):
        # Extract instance_name from kwargs or args
        global_variables = kwargs.pop('global_variables', {})
        processed_global_variables = {}
        for key in global_variables:
            if isinstance(global_variables[key], list):
                processed_global_variables[key] = global_variables[key]
            else:
                processed_global_variables[key] = [global_variables[key]]
        for single_chained_input in chained_input:
            #for each item in chained_input, add the global variables
            single_chained_input.update(processed_global_variables)
        output = original_run_method(self, chained_input)
        return output

    # Replace the original run method with the wrapped one
    setattr(cls, "run", wrapped_run)
    
    # Register the class in the registry
    class_registry[cls.__name__] = cls
    return cls


# Updated `Pipeline.run` with instance-specific params merged into `chained_input`
class Pipeline:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_id_counter = 0
        self.node_name_to_id = {}
        self.global_variables = {}

    def add(self, name: str, class_instance):
        self.node_id_counter += 1
        self.graph.add_node(self.node_id_counter, name=name, data=class_instance)
        self.node_name_to_id[name] = self.node_id_counter

    def connect(self, from_name: str, to_name: str):
        from_node_id = self.node_name_to_id.get(from_name)
        to_node_id = self.node_name_to_id.get(to_name)
        if from_node_id is None or to_node_id is None:
            raise ValueError("One or both of the node names provided do not exist.")
        self.graph.add_edge(from_node_id, to_node_id)

    def publish_pipeline_output(self, input_config, single_output):
        # The API Gateway endpoint URL
        url = 'https://drk3mkqa6b.execute-api.us-west-2.amazonaws.com/default/minimaxserver'
        api_key= os.environ["CREAO_API_KEY"]
        headers = {"Content-Type":"application/json", "x-api-key":api_key}
        # Payload to be sent to the Lambda function via API Gateway
        payload = {
            "single_output": single_output,
            "input_config": input_config,
            "pipeline_id": self.pipeline_id,
            "action": "pipeline_final_output"
        }
        # Send the request
        response = requests.post(url,headers=headers, json=payload)
        print("publish_pipeline_output reponse:", response.content)
        #print("reponse:", response.content)
        try:
            return response.json()
        except Exception as e:
            return {"error":e}

    def run(self):
        dict_list = self.run_datanode()
        for item in dict_list:
            print("input config:",item)            
            output = self.run_single(item)
            print("single_output:",output)
            self.publish_pipeline_output(item, output)

    def run_datanode(self):
        #instance_specific_params = instance_specific_params or {}

        if nx.is_directed_acyclic_graph(self.graph):
            execution_order = list(topological_sort(self.graph))
        else:
            raise ValueError("The graph is not a directed acyclic graph (DAG).")
        for node_id in execution_order:
            class_instance = self.graph.nodes[node_id]['data']
            node_name = self.graph.nodes[node_id]['name']
            # Run the class instance with the updated chained_input
            # output has type Dict[str, List[sr]]
            output_list = class_instance.run([], instance_name=node_name, validate_schema=False)
            output_list_force_list_value = []
            for item in output_list:
                for key in item:
                    value = item[key]
                    if not isinstance(value, list):
                        item[key] = [value]
                output_list_force_list_value.append(item)
            break
        return output_list_force_list_value

    def run_single(self, input_dict:Dict[str, List[str]]):
        #instance_specific_params = instance_specific_params or {}
        output_store = {}

        if nx.is_directed_acyclic_graph(self.graph):
            execution_order = list(topological_sort(self.graph))
        else:
            raise ValueError("The graph is not a directed acyclic graph (DAG).")
        for node_id in execution_order[1:]:
            class_instance = self.graph.nodes[node_id]['data']
            node_name = self.graph.nodes[node_id]['name']
            predecessors = list(self.graph.predecessors(node_id))
            predecessors_list = []
            for item in predecessors:
                if self.graph.nodes[item]['data'] in output_store:
                    predecessors_list.append(output_store[self.graph.nodes[item]['data']])
            print("predecessors_list:",predecessors_list)
            for item in predecessors_list:
                if item is None:
                    # if any of the predecessor is None, then return empty list
                    return []
            combinations = list(product(*predecessors_list))
            chained_input = []
            for item in combinations:
                temp_dict = {}
                for d in item:
                    temp_dict.update(d)
                chained_input.append(temp_dict)  
            if len(chained_input) == 0:
                chained_input = [input_dict]  
            # Run the class instance with the updated chained_input
            combined_global_varaibles = self.global_variables
            combined_global_varaibles.update(input_dict)
            output = class_instance.run(chained_input, global_variables = combined_global_varaibles, instance_name=node_name, validate_schema=False)
            # Store the output for downstream nodes
            output_store[class_instance] = output
        return output

    def to_dict(self):
        # Convert the pipeline into a dictionary format for serialization
        pipeline_dict = {"nodes": [], "connections": []}

        # Add nodes with their configuration
        for node_id, node_data in self.graph.nodes(data=True):
            class_instance = node_data["data"]
            class_dict = class_instance.__dict__
            if "llm" in class_dict:
                class_dict.pop("llm")
            node_dict = {
                "name": node_data["name"],
                "class": class_instance.__class__.__name__,
                "params": class_dict,  # Serialize the instance parameters
            }
            pipeline_dict["nodes"].append(node_dict)

        # Add connections between nodes
        for from_node, to_node in self.graph.edges():
            from_name = self.graph.nodes[from_node]["name"]
            to_name = self.graph.nodes[to_node]["name"]
            pipeline_dict["connections"].append({"from": from_name, "to": to_name})

        return pipeline_dict

    def save_to_yaml(self, file_path):
        """
        Save the pipeline to a YAML file.
        # TODO: @joshua need to make this function work with load_from_yaml, you could reference from load_from_yaml
        """
        pipeline_dict = self.to_dict()
        with open(file_path, "w") as yaml_file:
            yaml.dump(pipeline_dict, yaml_file)

    @staticmethod
    def from_dict(pipeline_dict, dataset_children_map, global_variables):
        pipeline = Pipeline()
        pipeline.pipeline_id = pipeline_dict.get("pipeline_id", "pipeline_id_default")
        pipeline.global_variables = global_variables
        pipeline.dataset_children_map = dataset_children_map

        # Reconstruct nodes
        for node in pipeline_dict["nodes"]:
            class_name = node["class"]
            class_instance = class_registry[class_name](**node["params"])
            pipeline.add(node["name"], class_instance)

        # Reconstruct connections
        for connection in pipeline_dict["connections"]:
            pipeline.connect(connection["from"], connection["to"])

        # Manually reinitialize necessary components
        for node_id in pipeline.graph.nodes:
            class_instance = pipeline.graph.nodes[node_id]['data']
            if isinstance(class_instance, DedupeComponent):
                class_instance.llm = Dedup()
            if isinstance(class_instance, LLMComponent):
                # Re-initialize CreaoLLM or OpenAILLM based on the service type
                if class_instance.service == "default":
                    class_instance.llm = CreaoLLM(bot_name="assistant", bot_content="assistant")
                elif class_instance.service == "openai":
                    class_instance.llm = OpenAILLM()

        return pipeline
    
    @staticmethod
    def create_pydantic_model(fields: List[Dict[str, Any]]) -> BaseModel:
        """
        Create a Pydantic model dynamically from a list of dictionaries representing fields.

        Args:
        - fields (List[Dict[str, Any]]): A list where each dict contains 'name' and 'type' keys.

        Returns:
        - A dynamically created Pydantic model class.
        """
        new_json_list = []
        for item in fields:
            if item["type"] == "list[str]":
                item["type"] = List[str]
            elif item["type"] == "str":
                item["type"] = str
            new_json_list.append(item)
        fields = new_json_list
        field_definitions = {field['name']: (field['type'], ...) for field in fields}
        return create_model('JsonBase', **field_definitions)
    
    @staticmethod
    def extract_json_schema(class_instance) -> Dict[str, Any]:
        # Generate the JSON schema
        # Generate the JSON schema
        json_schema = class_instance.schema()
        output_dict = json_schema["properties"]
        
        for key in class_instance.__fields__:
            output_dict[key].pop("title")
        return output_dict

    @staticmethod
    def extract_jinja2_varaibles(template_str:str)->List[str]:
        env = Environment()
        # Parse the template
        parsed_content = env.parse(template_str)
        variables = meta.find_undeclared_variables(parsed_content)
        return list(variables)

    def expand_run_config(self, config_dict, row_dict):
        for dataset_key in config_dict:
            dataset_value = config_dict[dataset_key]
            final_res = {}
            for component_key in dataset_value:
                component_value = dataset_value[component_key] # which is a list
                temp_dict = {}
                for item in component_value:
                    if item in self.global_variables:
                        temp_dict[item] = [self.global_variables[item]]
                    else:
                        if item in row_dict:
                            # there is a case item is actually from previous chain_input, so we don't need to add it here
                            temp_dict[item] = [row_dict[item]]
                final_res[component_key] = {"chained_input":[temp_dict]}
        return final_res
                
    @staticmethod
    def load_from_rf_json(file_path, rf_dict=None, global_variables=None):
        if rf_dict is None:
            with open(file_path, "r") as rf_file:
                rf_dict = json.load(rf_file)
        #then prepare nodes
        nodes = []
        id_to_name_dict = {}
        for node in rf_dict["nodes"]:
            id = node["id"]
            temp_dict = {}
            #prepare params
            params = {}
            node_data = node["data"]
            output_schema = node_data["output_schema"]
            temp_dict["name"] = node_data["label"]
            if "type" not in node:
                temp_dict["class"] = "LLMComponent"
                json_schema = Pipeline.extract_json_schema(Pipeline.create_pydantic_model(output_schema))
                params["json_schema"] = json_schema
            elif node["type"] == "dataNode":
                temp_dict["class"] = "HFDataComponent"
            elif node["type"] == "filterNode":
                temp_dict["class"] = "FilterComponent"
            elif node["type"] == "dedupeNode":
                temp_dict["class"] = "DedupeComponent"
            for key in node_data:
                if key == "output_schema" or key == "label":
                    continue
                params[key] = node_data[key]
            params["component_name"] = node_data["label"]
            temp_dict["params"] = params
            prompt_template  = node_data["prompt_template"] if "prompt_template" in node_data else ""
            id_to_name_dict[id] = {"label":node_data["label"],"class": temp_dict["class"], "prompt_template":prompt_template}
            nodes.append(temp_dict)
        #then prepare connections
        connections = []
        dataset_children_map = {}
        for edge in rf_dict["edges"]:
            from_node = id_to_name_dict[edge["source"]]
            to_node = id_to_name_dict[edge["target"]]
            if id_to_name_dict[edge["source"]]["class"] == "HFDataComponent":
                if from_node["label"] not in dataset_children_map:
                    dataset_children_map[from_node["label"]] = {to_node["label"]:Pipeline.extract_jinja2_varaibles(to_node["prompt_template"])} 
                else:
                    dataset_children_map[from_node["label"]][to_node["label"]] = Pipeline.extract_jinja2_varaibles(to_node["prompt_template"])
            connections.append({"from":from_node["label"], "to":to_node["label"]})
        #res = loaded_pipeline.run({"extract_interest":{"chained_input":[{"persona": "Student", "file_name": "news.txt", "passage": "this is a university rank"}]}})
        final_json = {"nodes":nodes, "connections":connections,"pipeline_id":rf_dict["pipeline_id"]}
        print("final_json:",final_json)
        return Pipeline.from_dict(final_json, dataset_children_map, global_variables)

    @staticmethod
    def load_from_yaml(file_path):
        # this function is not worked yet, it does not provide a dataset_children_map
        # TODO: @joshua need to fix this, you could reference the load_from_rf_json function
        with open(file_path, "r") as yaml_file:
            pipeline_dict = yaml.safe_load(yaml_file)
        return Pipeline.from_dict(pipeline_dict)

######BaseComponent
extract_poi_prompt_str = """\
You are given a Persona and a Passage. Your task is to immitate the persona and create a list interesting topics from the given passage.

<Persona>
{{persona}}
</Persona>

<Passage>
The following information is from a file with the title "{{file_name}}".

{{passage}}
</Passage>

Answer format - Generate a json with the following fields
- "list_of_interest": [<fill with 1-5 word desription>]

Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches. Show your thinking before giving an answer.
"""

class POISchema(BaseModel):
    list_of_interest: list[str]

@creao_component
class HFDataComponent:
    def __init__(self,hf_dataset_path: str, split: str = 'train', component_name:str="default", **kwargs):
        """
        Initialize HFDataComponent by downloading the dataset from Hugging Face.

        Args:
            hf_path (str): Path to the Hugging Face dataset (e.g., 'imdb').
            split (str): Which split of the dataset to use ('train', 'test', etc.).
        """
        self.hf_path = hf_dataset_path

    def _convert_to_dict_list(self, dataset) -> List[Dict[str, str]]:
        """
        Convert the Hugging Face dataset into a list of dictionaries.

        Returns:
            List[Dict[str, str]]: Processed data.
        """
        return [{key: str(value) for key, value in example.items()} for example in dataset]

    def run(self, chained_input: List[Dict[str, str]]) -> List[Dict[str, List[str]]]:
        """
        Return the downloaded data.

        Args:
            chained_input (List[Dict[str, str]]): Input from previous component.
        
        Returns:
            List[Dict[str, str]]: The dataset as a list of dictionaries.
        """
        print(f"Downloading dataset from {self.hf_path}...")
        dataset = load_dataset(self.hf_path, split="train")
        list_res = []
        for item in dataset:
            list_res.append(item)
        return list_res


@creao_component  # This decorator registers the class as a component in a pipeline framework
class FilterComponent:
    """
    FilterComponent is responsible for filtering data based on a specific condition applied to a designated column.
    The component can perform two types of filtering:
    1. Exact match filtering for strings or direct equality comparison.
    2. Numeric condition filtering for values that need to meet a specified numeric condition (e.g., >, <, >=).

    Attributes:
    - filtered_column (str): The name of the column on which the filter is applied.
    - condition_type (str): The type of filtering condition. It can be either "exact_match" or "numeric_condition".
    - condition_value (Union[str, int, float]): The value or condition used for filtering. It can be a string (for exact match) 
      or a numeric condition (e.g., "> 5", "== 10").
    - pipeline_id (str): Identifier for the pipeline this component belongs to. Defaults to "pipeline_id_default".
    - component_name (str): Name of the component, default is "FilterComponent".
    - **kwargs: Additional arguments that can be passed for customization.

    Methods:
    - run(chained_input: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      This method performs the filtering on the input data (a list of dictionaries). It processes each dictionary (or row)
      and filters it based on the specified conditions. It returns the filtered data as a list of dictionaries.

      - chained_input: The input data, which is expected to be a list of dictionaries where each dictionary represents a row or record.
      - filtered_output: The filtered data after applying the conditions.
      
      The method supports:
      - "exact_match" condition: Filters based on string equality or direct comparison to a specific value.
      - "numeric_condition" condition: Filters based on a numerical comparison using operators like >, <, >=, etc.

      Example usage:
      - If the condition_type is "exact_match" and condition_value is "apple", it will filter and return only the rows where 
        the specified column has the value "apple".
      - If the condition_type is "numeric_condition" and condition_value is "> 5", it will filter and return rows where the 
        numeric value in the specified column is greater than 5.

      If the column value cannot be found in the row or cannot be converted to a number for numeric conditions, the row is skipped.

    Example:
    component = FilterComponent(filtered_column="price", condition_type="numeric_condition", condition_value="> 50")
    filtered_data = component.run(input_data)
    """
    
    def __init__(self,
                 filtered_column: str,
                 condition_type: str = "exact_match",  # or "numeric_condition"
                 condition_value: Union[str, int, float] = None,
                 pipeline_id: str = "pipeline_id_default",
                 component_name: str = "FilterComponent",
                 **kwargs):
        self.filtered_column = filtered_column  # Column to apply the filter on
        self.condition_type = condition_type  # Type of condition, either "exact_match" or "numeric_condition"
        self.condition_value = condition_value  # Value or condition to filter against
        self.pipeline_id = pipeline_id  # ID of the pipeline this component belongs to
        self.component_name = component_name  # Name of the component

    def run(self, chained_input: List[Dict[str,List[str]]]) -> List[Dict[str,List[str]]]:
        for single_chained_input in chained_input:
            assert self.filtered_column in single_chained_input, f"Column '{self.filtered_column}' not found in the input data."
            filtered_output = []
            column_values = single_chained_input.get(self.filtered_column)  # Retrieve the value from the specified column
            # Handle different condition types
            for column_value in column_values:
                if self.condition_type == "exact_match":
                    if column_value == self.condition_value:  # Check for exact match
                        filtered_output.append(column_value)  # Add the row to the output if it matches

                elif self.condition_type == "numeric_condition":
                    try:
                        numeric_value = float(column_value)  # Convert the column value to a numeric value
                        if eval(f"{numeric_value} {self.condition_value}"):  # Evaluate the numeric condition
                            filtered_output.append(column_value)  # Add the row to the output if it meets the condition
                    except ValueError:
                        continue  # Skip if the value can't be converted to a number
            single_chained_input[self.filtered_column] = filtered_output
        return chained_input  # Return the filtered data


@creao_component
class DedupeComponent:
    def __init__(self,
                 dedup_column: str,
                 pipeline_id: str = "pipeline_id_default",
                 component_name:str="default",
                 **kwargs):
        self.pipeline_id = pipeline_id
        self.dedup_column = dedup_column
        self.component_name = component_name
        self.llm = Dedup()
    def convert_to_dict_of_lists(self, data: List[Dict[str, str]]) -> Dict[str, List[str]]:
        result = defaultdict(list)
        
        for entry in data:
            for key, value in entry.items():
                result[key].append(value)
        return result
    
    def run(self, chained_input: List[Dict[str,List[str]]]) -> List[Dict[str,List[str]]]:
        """
        Deduplicate the input texts.

        Args:
            chained_input (List[Dict[str, str]]): Input from previous component.
        Returns:
            List[Dict[str, str]]: Deduplicated texts.
        """
        for single_chained_input in chained_input:
            assert self.dedup_column in single_chained_input, f"Column '{self.dedup_column}' not found in the input data."
            for key in single_chained_input:
                if key == self.dedup_column:
                    texts = single_chained_input[key]
                    dedupe_res = self.llm.execute(texts)
                    single_chained_input[key] = dedupe_res
        return chained_input

@creao_component
class LLMComponent:
    def __init__(self, 
                 prompt_template: str = None, 
                 class_instance= None, 
                 service: str = "default", 
                 pipeline_id: str = "pipeline_id_default",
                 component_name:str="default", 
                 **kwargs):
        self.prompt_template = prompt_template
        self.component_name = component_name
        self.pipeline_id = pipeline_id
        json_schema = kwargs.pop('json_schema', None)
        self.type = kwargs.pop('type', None)
        if json_schema is None:
            if class_instance is not None:
                self.json_schema = Pipeline.extract_json_schema(class_instance)
            else:
                self.json_schema = None
        else:
            self.json_schema = json_schema
        self.service = service
        if self.service == "default":
            self.llm = CreaoLLM(bot_name="assistant", bot_content="assistant")
        elif self.service == "openai":
            self.llm = OpenAILLM()

    def run(self, chained_input:List[Dict[str,List[str]]])->List[Dict[str,List[str]]]:
        extract_jinja2_varaibles = Pipeline.extract_jinja2_varaibles(self.prompt_template)
        res_list = []
        for single_chain_input in chained_input:
            jinja_var_list = []
            for var in extract_jinja2_varaibles:
                jinja_var_list.append({var:single_chain_input[var]})
            jinja_inputs = convert_dict_list(jinja_var_list)
            prompt_template = Template(self.prompt_template)
            prompt_list = [(prompt_template.render(item),item) for item in jinja_inputs]
            for prompt, input_dict in prompt_list:
                if self.service == "default":
                    if self.json_schema is not None:
                        response_json = self.llm.invoke(prompt,self.json_schema,self.component_name,self.pipeline_id)
                    else:
                        response_json = self.llm.invoke(prompt,"",self.component_name,self.pipeline_id)
                    try:
                        if self.json_schema is not None:
                            raw_answer = json.loads(response_json["reply"]) 
                        else:
                            raw_answer = response_json["reply"]
                    except Exception as e:
                        print(f"ExtractPOI json decode error:{e}, response_json:{response_json}")
                        return None
                elif self.service == "openai":
                    try:
                        raw_answer = json.loads(self.llm.invoke(prompt))
                    except Exception as e:
                        print(f"ExtractPOI json decode error:{e}")
                        return None
                if self.service == "openai":
                    list_forcesd_answer = {"reply":[raw_answer]}
                else:
                    list_forcesd_answer = {}
                    for key in raw_answer:
                        if isinstance(raw_answer[key], list):
                            list_forcesd_answer[key] = raw_answer[key]
                        else:
                            list_forcesd_answer[key] = [raw_answer[key]]
                input_dict_value_list = {key:[input_dict[key]] for key in input_dict}
                list_forcesd_answer.update(input_dict_value_list)
                res_list.append(list_forcesd_answer)
        # currently res_list is with type List[Dict[str,str]], assume Dict[str,str] has exactly the same keys, 
        # we need to convert it to Dict[str, List[str]]
        return res_list
    

#extract_interest = LLMComponent(prompt_template=extract_poi_prompt_str, 
#                            class_instance=POISchema, 
#                            service="default", 
#                            pipeline_id="pipeline_id_default")



#interest_to_persona_prompt_str = """
#You are given a interest. Your task is to identify the persona that would be most interested in each topic.
#<interest>
#{{list_of_interest}}
#</interest>
#"""

#class Persona(BaseModel):
#    persona: str


#hfdataset = HFDataComponent(hf_path="creaoai/lilianweng_blog_url_synthetic_data_abstractive")

#res = hfdataset.run([])
#print(res)


#interest_to_persona = LLMComponent(prompt_template=interest_to_persona_prompt_str, 
#                            class_instance=Persona, 
#                            service="default", 
#                            pipeline_id="pipeline_id_default")

#pipeline = Pipeline()

# Add nodes
#pipeline.add("extract_interest", extract_interest)
#pipeline.add("interest_to_persona", interest_to_persona)
# Define connections
#pipeline.connect("extract_interest", "interest_to_persona")
#pipeline.save_to_yaml("pipeline.yaml")
#loaded_pipeline = Pipeline.load_from_rf_json("rf_json.json")
#res = loaded_pipeline.run()
#print("start to run")
#res = loaded_pipeline.run({"extract_interest":{"chained_input":[{"persona": "Student", "file_name": "news.txt", "passage": "this is a university rank"}]}})
#res = extract_interest.run([{"persona": "Student", "file_name": "news.txt", "passage": "this is a university rank"}])
#print(res)