
# FAIR report generator

Built on top of the excellent [pyfair](https://github.com/theonaunheim/pyfair)
library.

It turns a FAIR model specification into an image presenting either the Loss
Exceedance curve, or the probability distribution curve.  The idea is to allow
embedding these report images in other web applications by posting the
model specification to this service.

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

# Example

http://localhost:8080/fair/Overall%20risk?report=distribution&model=%7B%22name%22%3A%22Overall%20risk%22%2C%22parameters%22%3A%5B%7B%22name%22%3A%22tor-exit%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.25651593496984876%2C%22mode%22%3A0.5130318699396975%2C%22high%22%3A1.026063739879395%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A1539095.6098190926%2C%22mode%22%3A1795611.5447889413%2C%22high%22%3A2052127.47975879%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A2565159.3496984877%7D%7D%7D%2C%7B%22name%22%3A%22credential-theft%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.12111573868334374%2C%22mode%22%3A0.2422314773666875%2C%22high%22%3A0.484462954733375%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A726694.4321000625%2C%22mode%22%3A847810.1707834062%2C%22high%22%3A968925.90946675%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A1211157.3868334375%7D%7D%7D%2C%7B%22name%22%3A%22malware%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.021583498694971448%2C%22mode%22%3A0.043166997389942896%2C%22high%22%3A0.08633399477988579%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A129500.99216982869%2C%22mode%22%3A151084.49086480014%2C%22high%22%3A172667.98955977158%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A215834.98694971448%7D%7D%7D%5D%7D

http://localhost:8080/fair/Overall%20risk?report=report&model=%7B%22name%22%3A%22Overall%20risk%22%2C%22parameters%22%3A%5B%7B%22name%22%3A%22tor-exit%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.25651593496984876%2C%22mode%22%3A0.5130318699396975%2C%22high%22%3A1.026063739879395%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A1539095.6098190926%2C%22mode%22%3A1795611.5447889413%2C%22high%22%3A2052127.47975879%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A2565159.3496984877%7D%7D%7D%2C%7B%22name%22%3A%22credential-theft%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.12111573868334374%2C%22mode%22%3A0.2422314773666875%2C%22high%22%3A0.484462954733375%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A726694.4321000625%2C%22mode%22%3A847810.1707834062%2C%22high%22%3A968925.90946675%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A1211157.3868334375%7D%7D%7D%2C%7B%22name%22%3A%22malware%22%2C%22parameters%22%3A%7B%22Loss%20Event%20Frequency%22%3A%7B%22low%22%3A0.021583498694971448%2C%22mode%22%3A0.043166997389942896%2C%22high%22%3A0.08633399477988579%7D%2C%22Primary%20Loss%22%3A%7B%22low%22%3A129500.99216982869%2C%22mode%22%3A151084.49086480014%2C%22high%22%3A172667.98955977158%7D%2C%22Secondary%20Loss%22%3A%7B%22constant%22%3A215834.98694971448%7D%7D%7D%5D%7D

