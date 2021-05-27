import 'package:flutter/material.dart';
import "package:velocity_x/velocity_x.dart";

import 'package:Doormonitor/models/rest.dart';
import 'package:Doormonitor/routes.dart';
import 'package:Doormonitor/services/api_service.dart';
import 'package:Doormonitor/services/mqtt_service.dart';

import 'package:Doormonitor/models/rest.dart';

class DoorbellScreen extends StatefulWidget {
  @override
  _DoorbellScreenState createState() => _DoorbellScreenState();
}

class _DoorbellScreenState extends State<DoorbellScreen> {
  final ApiService api = ApiService();
  final MqttService mqtt = MqttService();
  late Future<int> _accessLevel;

  _DoorbellScreenState() {
    _accessLevel = api.getAccessLevel();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // appBar: AppBar(),
        body: FutureBuilder<int>(
            future: _accessLevel,
            builder: (BuildContext context, AsyncSnapshot<int> snapshot) {
              switch (snapshot.connectionState) {
                case ConnectionState.none:
                  return Row(
                    children: <Widget>[
                      Image.asset("images/1.jpg"),
                      OutlinedButton(
                          style: ButtonStyle(
                            foregroundColor:
                                MaterialStateProperty.all<Color>(Colors.blue),
                          ),
                          onPressed: () {
                            this.mqtt.ringDoorbell();
                          },
                          child: Text('Ringeklokke'))
                    ],
                  );
                case ConnectionState.waiting:
                  return new Text('Awaiting result...');
                default:
                  if (snapshot.hasError) {
                    return new Text('Error: ${snapshot.error}');
                  } else {
                    return Row(
                      children: <Widget>[
                        Image.asset("images/1.jpg"),
                        OutlinedButton(
                            style: ButtonStyle(
                              foregroundColor:
                                  MaterialStateProperty.all<Color>(Colors.blue),
                            ),
                            onPressed: () {
                              this.mqtt.ringDoorbell();
                            },
                            child: Text('Ringeklokke'))
                      ],
                    );
                  }
              }
            }));
  }
}
