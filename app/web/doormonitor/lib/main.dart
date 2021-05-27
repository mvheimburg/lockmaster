import 'package:flutter/material.dart';

import 'package:google_fonts/google_fonts.dart';
import "package:velocity_x/velocity_x.dart";

import 'package:Doormonitor/screens/doorbellscreen.dart';

import 'package:Doormonitor/routes.dart';

void main() {
  // runApp(VxState(store: DoormonitorStore(), child: DoormonitorApp()));

  runApp(DoormonitorApp());
}

// class DoormonitorStore extends VxStore {
//   final ApiService api = ApiService();
//   User? _selectedUser;
//   List<User> users = [];
// }

class DoormonitorApp extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _DoormonitorAppState();
}

class _DoormonitorAppState extends State<DoormonitorApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'VelocityX',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.red,
        textTheme: GoogleFonts.latoTextTheme(),
        appBarTheme: AppBarTheme(
            color: Vx.white,
            textTheme: GoogleFonts.latoTextTheme().apply(
              bodyColor: Vx.black,
            ),
            iconTheme: IconThemeData(color: Colors.black)),
      ),
      routeInformationParser: VxInformationParser(),
      routerDelegate: VxNavigator(
          notFoundPage: (uri, params) => MaterialPage(
                key: ValueKey('not-found-page'),
                child: Builder(
                  builder: (context) => Scaffold(
                    body: Center(
                      child: Text('Page ${uri.path} not found'),
                    ),
                  ),
                ),
              ),
          routes: {
            Routes.home: (uri, __) => MaterialPage(child: DoorbellScreen()),
          }),
    );
  }
}
