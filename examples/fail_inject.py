from fogbed.emulation import Services
from fogbed.experiment.local import FogbedExperiment
from fogbed.fails.controller import FailController
from fogbed.fails.models.availability import AvailabilityFail, AvailabilityMode
from fogbed.fails.models.disconnect import DisconnectFail
from fogbed.node.container import Container
from fogbed.resources import ResourceModel
from fogbed.resources.models import CloudResourceModel, EdgeResourceModel

Services(max_cpu=0.5, max_mem=512)
exp = FogbedExperiment()

edge = exp.add_virtual_instance('edge', EdgeResourceModel(max_cu=2, max_mu=256))
cloud = exp.add_virtual_instance('cloud', CloudResourceModel(max_cu=2, max_mu=512), AvailabilityFail(availability=0.8, slot_time=1, availability_mode=AvailabilityMode.DISCONNECT))

d1 = Container('d1', resources=ResourceModel.SMALL)
d2 = Container('d2', resources=ResourceModel.SMALL, fail_model=DisconnectFail(life_time=15))
d3 = Container('d3', resources=ResourceModel.SMALL)
d4 = Container('d4', resources=ResourceModel.SMALL)

exp.add_docker(d1, edge)
exp.add_docker(d2, edge)
exp.add_docker(d3, cloud)
exp.add_docker(d4, cloud)

exp.add_link(cloud, edge)
fail_controller = FailController(exp)

try:
    exp.start()
    fail_controller.start()
    exp.start_cli()
finally:
    fail_controller.stop()
    exp.stop()
