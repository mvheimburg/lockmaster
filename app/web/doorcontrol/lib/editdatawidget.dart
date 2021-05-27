import 'package:flutter/material.dart';
import 'package:doorcontrol/services/api_service.dart';
import 'models/rest.dart';

enum Gender { male, female }
enum Status { positive, dead, recovered }

class EditDataWidget extends StatefulWidget {
  EditDataWidget(this.user);

  final User user;

  @override
  _EditDataWidgetState createState() => _EditDataWidgetState();
}

class _EditDataWidgetState extends State<EditDataWidget> {
  _EditDataWidgetState();

  final ApiService api = ApiService();
  final _addFormKey = GlobalKey<FormState>();
  String id = '';
  final _nameController = TextEditingController();
  final _pinController = TextEditingController();
  final _macController = TextEditingController();
  final _endController = TextEditingController();
  final _accessLevelController = TextEditingController();

  @override
  void initState() {
    id = widget.user.id.toString();
    _nameController.text = widget.user.name;
    _pinController.text = widget.user.pin.toString();
    _macController.text = widget.user.mac.toString();
    _endController.text = widget.user.end.toString();
    _accessLevelController.text = widget.user.accessLevel.toString();
    super.initState();
  }

  void validateAndSave() {
    final FormState? form = _addFormKey.currentState;
    if (form != null) {
      if (form.validate()) {
        form.save();
        api.updateUser(
            id,
            User(
                name: _nameController.text,
                pin: int.parse(_pinController.text),
                mac: _macController.text,
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
        title: Text('Edit User'),
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
                              Text('MAC'),
                              TextFormField(
                                controller: _macController,
                                decoration: const InputDecoration(
                                  hintText: 'MAC',
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
                              TextFormField(
                                controller: _endController,
                                decoration: const InputDecoration(
                                  hintText: 'End',
                                ),
                                validator: (value) {
                                  if (value.toString().isEmpty ||
                                      value.toString() == 'null') {
                                    return 'Please enter end';
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
                              Text('AccessLevel'),
                              TextFormField(
                                controller: _accessLevelController,
                                decoration: const InputDecoration(
                                  hintText: 'AccessLevel',
                                ),
                                validator: (value) {
                                  if (value.toString().isEmpty ||
                                      value.toString() == 'null') {
                                    return 'Please enter Access Level';
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
