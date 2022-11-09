from fogbed.emulation import Services
from fogbed.experiment.local import FogbedExperiment
from fogbed.fails.controller import FailController
from fogbed.node.container import Container
from fogbed.resources import ResourceModel
from fogbed.resources.models import CloudResourceModel, EdgeResourceModel, FogResourceModel
from fogbed.fails.models.availability import AvailabilityFail, AvailabilityMode

Services(max_cpu=0.5, max_mem=2048)
exp = FogbedExperiment()

cloud = exp.add_virtual_instance('cloud', CloudResourceModel(max_cu=2, max_mu=512))
fog = exp.add_virtual_instance('fog', FogResourceModel(max_cu=2, max_mu=512))
edge = exp.add_virtual_instance('edge', EdgeResourceModel(max_cu=2, max_mu=1024), AvailabilityFail(availability=0.5, slot_time=2, availability_mode=AvailabilityMode.DISCONNECT))

gateway_cloud = Container('cloud', resources=ResourceModel.SMALL)
gateway_fog = Container('gate_fog', resources=ResourceModel.SMALL)
device = Container('device', resources=ResourceModel.SMALL, dimage='device')

exp.add_docker(gateway_cloud, cloud)
exp.add_docker(gateway_fog, fog)
exp.add_docker(device, edge)

exp.add_link(cloud, fog)
exp.add_link(fog, edge)

fail_controller = FailController(exp)

try:
    exp.start()
    fail_controller.start()
    exp.start_cli()
finally:
    fail_controller.stop()
    exp.stop()