import xml.etree.ElementTree as ET
from .models import Rule, ExtendedData


def parse_hazx_xml_str(xml_string: str) -> ExtendedData:
    root = ET.fromstring(xml_string)
    # 通过路径寻找下一个节点
    extended_data = root.find("extendedData")
    nextScenarioIndex = int(extended_data.attrib["nextScenarioIndex"])

    rules = []
    for rule_elem in extended_data.find("rules"):
        rule = Rule.from_xml_element(rule_elem)
        rules.append(rule)

    scenarios = [scenario.text for scenario in extended_data.find("scenarios")]
    customLTLs = [ltl.text for ltl in extended_data.find("customLTLs")]

    return ExtendedData(nextScenarioIndex, rules, scenarios, customLTLs)


def parse_hazx_file(hazx_file: str, encoding: str = "utf8"):
    with open(hazx_file, "r", encoding=encoding) as f:
        return parse_hazx_xml_str(f.read())
