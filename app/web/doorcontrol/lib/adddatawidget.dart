import 'package:flutter/material.dart';
import 'package:doorcontrol/services/api_service.dart';
import 'package:doorcontrol/models/rest.dart';
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';

// enum Gender { male, female }
// enum Status { positive, dead, recovered }

class AddDataWidget extends StatefulWidget {
  AddDataWidget();

  @override
  _AddDataWidgetState createState() => _AddDataWidgetState();
}

class _AddDataWidgetState extends State<AddDataWidget> {
  _AddDataWidgetState();

  final ApiService api = ApiService();
  final GlobalKey<FormState> _addFormKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _pinController = TextEditingController();
  final _uuidController = TextEditingController();
  final _endController = TextEditingController();
  final _accessLevelController = TextEditingController();
  // String status = 'positive';
  // Status _status = Status.positive;
  //
  void validateAndSave() {
    final FormState? form = _addFormKey.currentState;
    if (form != null) {
      if (form.validate()) {
        form.save();
        api.createUser(User(
            name: _nameController.text,
            pin: int.parse(_pinController.text),
            uuid: _uuidController.text,
            end: _endController.text,
            accessLevel: int.parse(_accessLevelController.text)));

        Navigator.pop(context);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Add User'),
      ),
      body: Form(
        key: _addFormKey,
        child: SingleChildScrollView(
          child: Container(
            padding: EdgeInsets.all(20.0),
            child: Card(
                child: Container(
                    padding: EdgeInsets.all(10.0),
                    width: 440,
                    child: Column(
                      children: <Widget>[
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              Text('Full Name'),
                              TextFormField(
                                controller: _nameController,
                                decoration: const InputDecoration(
                                  hintText: 'Full Name',
                                ),
                                validator: (value) {
                                  if (value.toString().isEmpty ||
                                      value.toString() == 'null') {
                                    return 'Please enter full name';
                                  }
                                  return null;
                                },
                                onChanged: (value) {},
                              ),
                            ],
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              Text('Pin'),
                              TextFormField(
                                controller: _pinController,
                                decoration: const InputDecoration(
                                  hintText: 'Pin',
                                ),
                                keyboardType: TextInputType.number,
                                validator: (value) {
                                  if (value.toString().isEmpty) {
                                    return null;
                                  }
                                },
                                onChanged: (value) {},
                              ),
                            ],
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              Text('uuid'),
                              TextFormField(
                                controller: _uuidController,
                                decoration: const InputDecoration(
                                  hintText: 'uuid',
                                ),
                                validator: (value) {
                                  if (value.toString().isEmpty) {
                                    return null;
                                  }
                                },
                                onChanged: (value) {},
                              ),
                            ],
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              Text('End'),
                              TextButton(
                                  onPressed: () {
                                    DatePicker.showDatePicker(
                                      context,
                                      showTitleActions: true,
                                      minTime: DateTime.now(),
                                      maxTime: DateTime(2099, 31, 12, 24),
                                      currentTime: DateTime.now(),
                                      locale: LocaleType.en,
                                      onConfirm: (date) {
                                        _endController.text = date.toString();
                                        DatePicker.showTimePicker(context,
                                            showTitleActions: true,
                                            onConfirm: (date) {
                                          _endController.text = date.toString();
                                        }, currentTime: DateTime.now());
                                      },
                                    );
                                  },
                                  child: Text(
                                    _endController.text,
                                    style: TextStyle(color: Colors.blue),
                                  )),
                            ],
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              Text('AccessLevel'),
                              TextFormField(
                                controller: _accessLevelController,
                                decoration: const InputDecoration(
                                  hintText: 'AccessLevel',
                                ),
                                validator: (value) {
                                  if (value.toString().isEmpty ||
                                      value.toString() == 'null') {
                                    return 'Please enter accessLevel';
                                  }
                                  return null;
                                },
                                onChanged: (value) {},
                              ),
                            ],
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(0, 0, 0, 10),
                          child: Column(
                            children: <Widget>[
                              RaisedButton(
                                splashColor: Colors.red,
                                onPressed: () {
                                  validateAndSave();
                                },
                                child: Text('Save',
                                    style: TextStyle(color: Colors.white)),
                                color: Colors.blue,
                              )
                            ],
                          ),
                        ),
                      ],
                    ))),
          ),
        ),
      ),
    );
  }
}
