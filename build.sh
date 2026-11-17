#!/usr/bin/env bash

poetry install --no-root --without dev

poetry run flask db upgrade
