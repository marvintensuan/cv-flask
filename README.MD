# My Curriculum Vitae Website (now in Flask).

**Related repository:** [cv-django](https://github.com/marvintensuan/cv-django)

## Overview

There were many reasons why I had to create a Flask version of my `cv-django` project. First and foremost is the _cost_. Cloud SQL instances are expensive, and for an app whose sole purpose is to serve static files, I didn't think it's worth it.

Hence why I chose `Flask` and `Firestore`. Flask not being bulky means less storage use and Firestore is a serverless service with free tier. Django also doesn't natively support document databases.

Another thing that's different this time is the way I deployed the app. This website is deployed directly from VSCode (instead of using the built-in cloud shell editor).

## How To Build

*TODO*

## Project History

. . . (continued from [cv-django](https://github.com/marvintensuan/cv-django#History) README.)

2021-02-12 &mdash; deployed https://mrvn-flask-service-qmtxf7rosq-de.a.run.app/

