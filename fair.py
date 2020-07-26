
import pyfair
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np
import scipy.stats as stats

lef_points = 50
risk_bins = 25
pdf_points = 50

# all returns map of models
def load_model(spec, all):

    name = spec["name"]
    params = spec["parameters"]
    if "simulations" in spec:
        simul=int(spec["simulations"])
    else:
        simul=10000

    if type(params) == dict:

        model = pyfair.FairModel(name=name, n_simulations=simul)
        model.bulk_import_data(params)
        all[name] = model
        return model

    if type(params) == list:

        models = [
            load_model(m, all) for m in params
        ]
        metamodel = pyfair.FairMetaModel(name=name, models=models)
        all[name] = metamodel
        return metamodel

    raise RuntimeError("Bad model parameters")

def distribution_image(models):

    dc = pyfair.report.distribution.FairDistributionCurve(
        [models[k] for k in models]
    )
    fig, ax = dc.generate_image()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    ilen = buf.tell()
    buf.seek(0)
    data = buf.read(ilen)

    return data, "image/png"

def exceedence_image(models):

    dc = pyfair.report.exceedence.FairExceedenceCurves(
        [models[k] for k in models]
    )
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

def curves(model, all_models):

    output = {}

    results = model.export_results()
    all_risk = results["Risk"]
    all_max = all_risk.max()

    prob_space = pd.Series(np.linspace(0, all_max, lef_points))

    for name in all_models:

        model = all_models[name]

        model_out = {}
        
        risk = model.export_results()["Risk"]
        risk_max = risk.max()

        model_out["summary"] = {
            'mean': risk.mean(),
            'min': risk.min(),
            'max': risk.max(),
            'stddev': risk.std()
        }

        space = pd.Series(np.linspace(0, risk_max, lef_points))

        prob = space.map(lambda x: stats.percentileofscore(risk, x))
        loss = space.map(lambda value: (value < risk).mean()) * 100

        model_out["prob"] = [
            [space[v], prob[v]] for v in range(0, len(space))
        ];

        model_out["loss"] = [
            [space[v], loss[v]] for v in range(0, len(space))
        ];

        beta_curve = stats.beta(*stats.beta.fit(risk))

        pdf_space = np.linspace(0, risk_max, pdf_points)
        pdf = beta_curve.pdf(pdf_space)

        model_out["pdf"] = [
            [pdf_space[v], pdf[v]]
            for v in range(0, len(pdf_space))
        ]

        hist = np.histogram(risk, bins=risk_bins)

        model_out["risk"] = [
            [hist[1][v], int(hist[0][v])]
            for v in range(0, risk_bins)
        ];

        output[name] = model_out

    return output

def loss(model, all_models):

    output = {}

    results = model.export_results()

    for name in all_models:

        model = all_models[name]

        model_out = {}
        
        risk = model.export_results()["Risk"]
        risk_max = risk.max()

        space = pd.Series(np.linspace(0, risk_max, lef_points))

        prob = space.map(lambda x: stats.percentileofscore(risk, x))
        loss = space.map(lambda value: (value < risk).mean()) * 100

        model_out["prob"] = [
            [space[v], prob[v]] for v in range(0, len(space))
        ];

        model_out["loss"] = [
            [space[v], loss[v]] for v in range(0, len(space))
        ];

        output[name] = model_out

    return output



def summary(model, all_models):

    output = {}

    results = model.export_results()

    for name in all_models:

        model = all_models[name]

        model_out = {}
        
        risk = model.export_results()["Risk"]
        risk_max = risk.max()

        model_out["summary"] = {
            'mean': risk.mean(),
            'min': risk.min(),
            'max': risk.max(),
            'stddev': risk.std()
        }

        output[name] = model_out

    return output



def pdf(model, all_models):

    output = {}

    results = model.export_results()
    all_risk = results["Risk"]
    all_max = all_risk.max()

    for name in all_models:

        model = all_models[name]

        model_out = {}
        
        risk = model.export_results()["Risk"]
        risk_max = risk.max()

        beta_curve = stats.beta(*stats.beta.fit(risk))

        pdf_space = np.linspace(0, risk_max, pdf_points)
        pdf = beta_curve.pdf(pdf_space)

        model_out["pdf"] = [
            [pdf_space[v], pdf[v]]
            for v in range(0, len(pdf_space))
        ]

        output[name] = model_out

    return output

def risk(model, all_models):

    output = {}

    for name in all_models:

        model = all_models[name]

        model_out = {}
        
        risk = model.export_results()["Risk"]

        hist = np.histogram(risk, bins=risk_bins)

        model_out["risk"] = [
            [hist[1][v], int(hist[0][v])]
            for v in range(0, risk_bins)
        ];

        output[name] = model_out

    return output
