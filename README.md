# JuTrack-Dashboard
## v2.0
Dashboard for the digital biomarker platform

### Adding a sensor to the dashboard

* add the sensorname to the Array `sensors_per_modality_dict` in `study/__init__.py`
* add the column names `sensorname n_batches` and `sensorname last_time_received` to the Array `table_columns` in the same file
