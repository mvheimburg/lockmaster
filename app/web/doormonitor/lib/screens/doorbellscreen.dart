import 'package:flutter/material.dart';

import 'package:doormonitor/services/api_service.dart';
import 'package:carousel_slider/carousel_slider.dart';
// import 'package:carousel_slider/carousel_options.dart';
import "package:velocity_x/velocity_x.dart";
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:passcode_screen/circle.dart';
import 'package:passcode_screen/keyboard.dart';
import 'package:passcode_screen/passcode_screen.dart';
import 'package:doormonitor/routes.dart';

final List<String> imgList = ["images/1.jpg", "images/2.jpg"];

class DoorbellScreen extends StatefulWidget {
  @override
  _DoorbellScreenState createState() => _DoorbellScreenState();
}

class _DoorbellScreenState extends State<DoorbellScreen> {
  final ApiService api = ApiService();
  late Future<int> _accessLevel;
  final StreamController<bool> _verificationNotifier =
      StreamController<bool>.broadcast();

  _DoorbellScreenState() {
    // _accessLevel = api.getAccessLevel();
    _accessLevel = dummy();
  }

  Future<int> dummy() async {
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: FutureBuilder<int>(
            future: _accessLevel,
            builder: (BuildContext context, AsyncSnapshot<int> snapshot) {
              switch (snapshot.connectionState) {
                case ConnectionState.none:
                  return Row(
                    children: <Widget>[
                      CarouselSlider(
                          items: imgList
                              .map((item) => Container(
                                      child: GestureDetector(
                                    onDoubleTap: () {
                                      _showLockScreen(context,
                                          opaque: false,
                                          cancelButton: Text(
                                            'Cancel',
                                            style: const TextStyle(
                                                fontSize: 16,
                                                color: Colors.white),
                                            semanticsLabel: 'Cancel',
                                          ));
                                    },
                                    child: Center(
                                        child: Image.asset(item,
                                            fit: BoxFit.cover, width: 480)),
                                  )))
                              .toList(),
                          options: CarouselOptions(
                            // height: 600,
                            aspectRatio: 1,
                            // viewportFraction: 1,
                            // initialPage: 0,
                            // enableInfiniteScroll: true,
                            reverse: false,
                            autoPlay: true,
                            autoPlayInterval: Duration(seconds: 10),
                            autoPlayAnimationDuration:
                                Duration(milliseconds: 800),
                            autoPlayCurve: Curves.fastOutSlowIn,
                            // enlargeCenterPage: true,
                            scrollDirection: Axis.horizontal,
                          )),
                      // Image.asset("images/1.jpg"),
                      // Expanded
                      Container(
                          alignment: Alignment.center,
                          child: Center(
                              child: IconButton(
                            icon: const Icon(Icons.doorbell),
                            iconSize: 200,
                            color: Colors.blueAccent,
                            onPressed: () {
                              this.api.ringDoorbell();
                            },
                          ))),
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
                        CarouselSlider(
                            items: imgList
                                .map((item) => Container(
                                        child: GestureDetector(
                                      onDoubleTap: () {
                                        _showLockScreen(context,
                                            opaque: false,
                                            cancelButton: Text(
                                              'Cancel',
                                              style: const TextStyle(
                                                  fontSize: 16,
                                                  color: Colors.white),
                                              semanticsLabel: 'Cancel',
                                            ));
                                      },
                                      child: Center(
                                          child: Image.asset(item,
                                              fit: BoxFit.cover, width: 480)),
                                    )))
                                .toList(),
                            options: CarouselOptions(
                              // height: 600,
                              aspectRatio: 1,
                              // viewportFraction: 1,
                              // initialPage: 0,
                              // enableInfiniteScroll: true,
                              reverse: false,
                              autoPlay: true,
                              autoPlayInterval: Duration(seconds: 10),
                              autoPlayAnimationDuration:
                                  Duration(milliseconds: 800),
                              autoPlayCurve: Curves.fastOutSlowIn,
                              // enlargeCenterPage: true,
                              scrollDirection: Axis.horizontal,
                            )),
                        // Image.asset("images/1.jpg"),
                        // Expanded(
                        Container(
                            alignment: Alignment.center,
                            child: Center(
                                child: IconButton(
                              icon: const Icon(Icons.doorbell),
                              iconSize: 200,
                              color: Colors.blueAccent,
                              onPressed: () {
                                this.api.ringDoorbell();
                              },
                            ))),
                      ],
                    );
                  }
              }
            }));
  }

  _showLockScreen(
    BuildContext context, {
    required bool opaque,
    CircleUIConfig? circleUIConfig,
    KeyboardUIConfig? keyboardUIConfig,
    required Widget cancelButton,
    List<String>? digits,
  }) {
    Navigator.push(
        context,
        PageRouteBuilder(
          opaque: opaque,
          pageBuilder: (context, animation, secondaryAnimation) =>
              PasscodeScreen(
            title: Text(
              'Enter App Passcode',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontSize: 28),
            ),
            circleUIConfig: circleUIConfig,
            keyboardUIConfig: keyboardUIConfig,
            passwordEnteredCallback: _onPasscodeEntered,
            cancelButton: cancelButton,
            deleteButton: Text(
              'Delete',
              style: const TextStyle(fontSize: 16, color: Colors.white),
              semanticsLabel: 'Delete',
            ),
            shouldTriggerVerification: _verificationNotifier.stream,
            backgroundColor: Colors.black.withOpacity(0.8),
            cancelCallback: _onPasscodeCancelled,
            digits: digits,
            passwordDigits: 4,
            // bottomWidget: _buildPasscodeRestoreButton(),
          ),
        ));
  }

  _onPasscodeEntered(String enteredPasscode) {
    // bool isValid = storedPasscode == enteredPasscode;
    _accessLevel = api.getAccessLevelByPin(enteredPasscode);
    _accessLevel.then((value) {
      bool isValid = false;
      if (value > 0) {
        isValid = true;
      }
      _verificationNotifier.add(isValid);

      // if (isValid) {
      //   setState(() {
      //     this.isAuthenticated = isValid;
      //   });
    });
  }

  _onPasscodeCancelled() {
    Navigator.maybePop(context);
  }

  @override
  void dispose() {
    _verificationNotifier.close();
    super.dispose();
  }
}
