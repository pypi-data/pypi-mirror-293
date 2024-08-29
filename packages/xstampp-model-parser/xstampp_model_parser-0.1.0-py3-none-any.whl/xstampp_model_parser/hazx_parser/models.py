from typing import List, Optional
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from xml.etree.ElementTree import Element


@dataclass
class Rule(DataClassJsonMixin):
    ruleID: str
    ruleNR: int
    criticalCombies: str
    refinedSafetyRule: str
    refinedUCA: str
    refinedSC: str
    ltlProp: str
    type: str
    relatedCaID: str
    relatedUCAIDs: Optional[str] = field(default="")

    @classmethod
    def from_xml_element(cls, elem: Element):
        return cls(
            ruleID=elem.find("ruleID").text,
            ruleNR=int(elem.find("ruleNR").text),
            criticalCombies=elem.find("criticalCombies").text,
            refinedSafetyRule=elem.find("RefinedSafetyRule").text,
            refinedUCA=elem.find("refinedUCA").text,
            refinedSC=elem.find("refinedSC").text,
            ltlProp=elem.find("ltlProp").text,
            type=elem.find("type").text,
            relatedUCAIDs=(
                elem.find("relatedUCAIDs").text
                if elem.find("relatedUCAIDs") is not None
                else ""
            ),
            relatedCaID=elem.find("relatedCaID").text,
        )


@dataclass
class ExtendedData(DataClassJsonMixin):
    nextScenarioIndex: int
    rules: List[Rule]
    scenarios: List[str] = field(default_factory=list)
    customLTLs: List[str] = field(default_factory=list)

    @classmethod
    def from_xml_element(cls, elem: Element):
        nextScenarioIndex = int(elem.attrib["nextScenarioIndex"])

        rules = []
        for rule_elem in elem.find("rules"):
            rule = Rule.from_xml_element(rule_elem)
            rules.append(rule)

        scenarios = [scenario.text for scenario in elem.find("scenarios")]
        customLTLs = [ltl.text for ltl in elem.find("customLTLs")]

        return cls(nextScenarioIndex, rules, scenarios, customLTLs)
