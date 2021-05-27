import 'package:flutter/material.dart';
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';
// import 'package:flutter_dropdown/flutter_dropdown.dart';

import 'package:doorcontrol/models/rest.dart';
import 'package:doorcontrol/services/api_service.dart';

class AddUserScreen extends StatefulWidget {
  @override
  _AddUserScreenState createState() => _AddUserScreenState();
}

class _AddUserScreenState extends State<AddUserScreen> {
  final ApiService api = ApiService();
  final GlobalKey<FormState> _addFormKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _pinController = TextEditingController();
  final _macController = TextEditingController();
  final _endController = TextEditingController();
  var _endControllerSupport = DateTime.now();
  final _accessLevelController = TextEditingController();
  // String status = 'positive';
  // Status _status = Status.positive;

  String _chosenValue = "Velg MAC fra liste";

  Future<List<Candidate>>? _candidateList;

  var timetext = Text('Velg tid');

  _AddUserScreenState() {
    this._candidateList = ApiService().getCandidates();
  }

  //
  void validateAndSave() {
    final FormState? form = _addFormKey.currentState;
    if (form != null) {
      if (form.validate()) {
        form.save();
        api.createUser(User(
            name: _nameController.text,
            pin: int.parse(_pinController.text),
            mac: _macController.text,
            end: _endController.text,
            accessLevel: int.parse(_accessLevelController.text)));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
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
                            child: FutureBuilder<List<Candidate>>(
                                future: _candidateList,
                                builder: (BuildContext context,
                                    AsyncSnapshot<List<Candidate>> snapshot) {
                                  switch (snapshot.connectionState) {
                                    case ConnectionState.none:
                                      return Column(
                                        children: <Widget>[
                                          Text(
                                              'MAC not available. Enter manually if wanted'),
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
                                              onChanged: (value) {}),
                                        ],
                                      );
                                    case ConnectionState.waiting:
                                      return new Text('Awaiting result...');
                                    default:
                                      if (snapshot.hasError) {
                                        return new Text(
                                            'Error: ${snapshot.error}');
                                      } else {
                                        var candidateList = snapshot.data!;
                                        return Column(children: <Widget>[
                                          Text('MAC'),
                                          // DropDown<Candidate>(
                                          //     items: candidateList,
                                          //     //                initialValue: selectedPerson,
                                          //     hint: Text("Select MAC"),
                                          //     initialValue: candidateList.first,
                                          //     onChanged: (Candidate c) {
                                          //       print(c.mac);
                                          //       setState(() {
                                          //         _macController.text = c.mac;
                                          //       });
                                          //     })
                                          DropdownButton<String>(
                                              value: _chosenValue,
                                              hint: Text("Velg MAC fra liste"),
                                              onChanged: (String? value) {
                                                setState(() {
                                                  _chosenValue = value!;
                                                });

                                                _macController.text =
                                                    _chosenValue;
                                              },
                                              items: candidateList
                                                  .map((Candidate candidate) {
                                                return new DropdownMenuItem<
                                                    String>(
                                                  value:
                                                      candidate.mac.toString(),
                                                  child: new Text(
                                                      "${candidate.mac} with rssi ${candidate.rssi}"),
                                                );
                                              }).toList())
                                        ]);
                                      }
                                  }
                                })),
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
                                        DatePicker.showTimePicker(context,
                                            showTitleActions: true,
                                            onConfirm: (time) {
                                          _endController.text = DateTime(
                                                  date.year,
                                                  date.month,
                                                  date.day,
                                                  time.hour,
                                                  time.minute,
                                                  time.second)
                                              .toString();
                                          setState(() {
                                            timetext =
                                                Text("${_endController.text}");
                                          });
                                        }, currentTime: DateTime.now());
                                        setState(() {
                                          timetext =
                                              Text("${_endController.text}");
                                        });
                                      },
                                    );
                                  },
                                  child: Text(
                                    'Tidsvelger',
                                    style: TextStyle(color: Colors.blue),
                                  )),
                              timetext
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
