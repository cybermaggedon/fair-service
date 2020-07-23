
# FAIR report generator

Built on top of the excellent [pyfair](https://github.com/theonaunheim/pyfair)
library.

It turns a FAIR model specification into an image presenting either the Loss
Exceedance curve, or the probability distribution curve.

It is a web server which you feed FAIR model data, either as a POST or
in the URL which returns a png image.

This isn't production ready, but you might find it
useful for a demo, which is what I'm doing.

## To use

Run the `evs-fair` Python script.  It listens on port 8080.  Or, run
`make` to build a Docker container.

You may need to install... `pip3 install pyfair scipy pandas matplotlib`.

## Invocation

### Create the FAIR model parameters

Take your FAIR model parameters and put them in a map e.g.
```
{
    "Loss Event Frequency": { "mean": 0.3, "stdev": 0.1 },
    "Loss Magnitude": { "constant": 5_000_000 }
}
```

### Create a model

A model object is a map with a `name` parameter containing a name
which will appear in the report, and a `parameters` parameter containing the
map made in the previous section e.g.
```
{
    "name": "my model",
    "parameters": {
	"Loss Event Frequency": { "mean": 0.3, "stdev": 0.1 },
	"Loss Magnitude": { "constant": 5000000 }
    }
}
```

### Layer models

You can use a single model as input, or create a metamodel by combining
multiple model objects.  To create a metamodel, put multiple models in
an array as the `parameter` value. e.g.
```
{
    "name": "my metamodel",
    "parameters": [
	{
	    "name": "my model",
	    "parameters": {
		"Loss Event Frequency": { "mean": 0.3, "stdev": 0.1 },
		"Loss Magnitude": { "constant": 5000000 }
	    }
	},
	{
	    "name": "my model 2",
	    "parameters": {
		"Loss Event Frequency": { "mean": 0.5, "stdev": 0.2 },
		"Loss Magnitude": { "constant": 250000 }
	    }
	}
    ]
}
```

### Create the URL

URL-encode the model and provide it in a URL of the form...
```
    /fair?report=...&model=...
```

You set the report parameter to be `exceedence` or `distribution` depending
on the type of report you want.  Model is your URL-encoded model.

Feed the URL to this service, if everything works, you get a payload
back, MIME-type is `image/png` and the payload is the report PNG image.

# Todo

This isn't production ready.  It's a single-threaded HTTP server which
only handles one connection at once, this is especially bad as the FAIR
calculations require crunching a lot of numbers.

