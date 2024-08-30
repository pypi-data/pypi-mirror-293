from oemof import solph
import pandas as pd

es = solph.EnergySystem(
    timeindex=solph.create_time_index(2022, 1, 3), infer_last_interval=False
)

bus = solph.Bus(label="Bus")
source = solph.components.Source(
    label="Source",
    outputs={bus: solph.Flow(variable_costs=[0.1, 0.3, 0.2])},
)
sink = solph.components.Sink(
    label="Sink", inputs={bus: solph.Flow(fix=[25, 30, 50], nominal_value=100)}
)

es.add(bus, source, sink)

model = solph.Model(es)

df = pd.DataFrame(
    {
        k: v.variable_costs
        for k, v in model.flows.items()
        if v.variable_costs is not None
    }
)

print(df)
