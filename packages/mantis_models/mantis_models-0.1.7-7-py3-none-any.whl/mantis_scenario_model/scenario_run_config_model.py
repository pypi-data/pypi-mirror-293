# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from pydantic import BaseModel
from pydantic import NonNegativeInt

from .log_collector_model import LogCollectorLocation
from .log_collector_model import LogCollectorType


class LogCollectorInstanceLocation(BaseModel):
    location_type: LogCollectorLocation
    """The type of log collector location, which can be either:

* ``node_name``: allows to deploy a log collector on specific node names (e.g. "Client1").
* ``new_node``: allows to deploy a log collector on a new node (e.g. a dedicated 'logstash' node).
* ``system_type``: allows to deploy a log collector on a specific system (e.g. "windows").
* ``operating_system``: allows to deploy a log collector on a specific Windows version (e.g. "Windows 10").
* ``external``: describes an external SIEM, XDR or log collector.
"""
    value: str
    """The log collector instance location name (e.g. "Client1")."""


class LogCollectorInstanceOutput(BaseModel):
    instance_name: str
    """The log collector instance output name (e.g. "logstash01")."""
    collector_name: str
    """The log collector output name (e.g. "logstash")."""
    collector_type: LogCollectorType
    """The log collector type, which can be either:

* ``agent``: an agent deployed on a node.
* ``aggregator``: a log aggregator.
* ``probe``: a probe to collect network traffic.
* ``visualization``: a log visualization software.
* ``external``: an external product to collect logs.
"""


class LogCollectorInstance(BaseModel):
    instance_name: str
    """The log collector instance name (e.g. "logstash01")."""
    collector_name: str
    """The log collector output name (e.g. "logstash")."""
    collector_type: LogCollectorType
    """The log collector type, which can be either:

* ``agent``: an agent deployed on a node.
* ``aggregator``: a log aggregator.
* ``probe``: a probe to collect network traffic.
* ``visualization``: a log visualization software.
* ``external``: an external product to collect logs.
"""
    location: List[LogCollectorInstanceLocation]
    """A list of log collector instance locations."""
    # input: List[LogCollectorInput] = []  # Currently not activated
    output: List[LogCollectorInstanceOutput] = []
    """A list of log collector instance outputs."""
    user_config: Dict = {}
    """A list of user configuration variables of the form key/values. This can be used to transmit API keys."""
    user_config_expert_mode: Dict = {}
    """In expert mode, a list of user configuration variables of the form key/values. This can be used to transmit specific log collector configurations."""


class ContentType(str, Enum):
    KILLCHAIN = "KILLCHAIN"
    ATTACK = "ATTACK"
    TOPOLOGY = "TOPOLOGY"
    BASEBOX = "BASEBOX"


class ScenarioExecutionMode(str, Enum):
    automatic = "automatic"
    step_by_step = "step_by_step"
    custom = "custom"  # Need step_waiting_list


class PositionStep(str, Enum):
    before = "before"
    after = "after"


class ScenarioRunConfig(BaseModel):
    """ScenarioRunConfig object configuration."""

    config_name: str = "default"
    """The name of the configuration."""

    content_type: Optional[ContentType] = None
    """The type of content to execute, which can be either:

* ``KILLCHAIN``: in order to run a complete scenario with a cyber killchain.
* ``ATTACK``: in order to run a unitary attack.
* ``TOPOLOGY``: in order to launch a topology only.
* ``BASEBOX``: in order to launch a specific basebox.
    """

    content_name: Optional[str] = None
    """The name of the content to execute.
    """

    scenario_config_name: Optional[str] = None
    """The name of the scenario topology name to run."""

    internet_connectivity: bool = False
    """Tells if internet access should be provided on SwitchMonitoring lan. Internet access is mandatory for example when using external SIEM / XDR solutions."""

    net_capture: bool = False
    """Tells if PCAP will be generated in datasets and traffic mirrored to potential probes."""

    forensic_artifacts: bool = False
    """Tells if forensic artifacts will be generated in datasets."""

    create_dataset: bool = False
    """Tells if a dataset will be created after scenario execution."""

    user_activity_background: bool = False
    """Tells to produce background random user activities on desktops."""

    log_collectors: List[LogCollectorInstance] = []
    """Specifies the supervision architecture to implement in terms of log collection, aggregation, and visualization."""

    random_waiting_minutes: Tuple[NonNegativeInt, NonNegativeInt] = [
        0,
        0,
    ]
    """Waiting range in minutes between attack steps."""

    scenario_execution_mode: ScenarioExecutionMode = ScenarioExecutionMode.automatic
    """Defines the execution mode of the scenario. The execution mode can be either:

* ``automatic``: the various scenario steps are executed one after the other without pause (default behavior).
* ``step_by_step``: a pause occurs between each scenario step.
* ``custom``: a list of scenario attacks for which a pause is required is defined in the ``step_waiting_list`` attribute.
"""

    step_waiting_list: List[str] = []
    """Defines at which steps to pause scenario execution (none by default)."""

    max_duration: int = 55 * 60
    """Define max duration of a simulation in minutes (55 minutes by
    default). If set to 0, this means no timeout for the simulation.
    """
