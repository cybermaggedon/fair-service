
import pyfair
import matplotlib.pyplot as plt
import io
import pandas as pd

# Returns list of models
def load_model(spec, all):

    name = spec["name"]
    params = spec["parameters"]
    if "simulations" in spec:
        simul=int(spec["simulations"])
    else:
        simul=10_000

    if type(params) == dict:

        model = pyfair.FairModel(name=name, n_simulations=simul)
        model.bulk_import_data(params)
        all.append(model)
        return model

    if type(params) == list:

        models = [
            load_model(m, all) for m in params
        ]
        metamodel = pyfair.FairMetaModel(name=name, models=models)
        all.append(metamodel)
        return metamodel

    raise RuntimeError("Bad model parameters")

def distribution_image(models):

    dc = pyfair.report.distribution.FairDistributionCurve(models)
    fig, ax = dc.generate_image()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    ilen = buf.tell()
    buf.seek(0)
    data = buf.read(ilen)

    return data, "image/png"

def exceedence_image(models):

    dc = pyfair.report.exceedence.FairExceedenceCurves(models)
    fig, ax = dc.generate_image()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    ilen = buf.tell()
    buf.seek(0)
    data = buf.read(ilen)

    return data, "image/png"

def summary(model):

    results = model.export_results().T

    summary = pd.DataFrame({
        'mean': results.mean(axis=1), 
        'stdev': results.std(axis=1),
        'min': results.min(axis=1),
        'max': results.max(axis=1),
    })

    return summary



