import 'package:flutter/material.dart';
import 'dart:async';

import 'package:google_fonts/google_fonts.dart';
import "package:velocity_x/velocity_x.dart";

import 'package:doorcontrol/adddatawidget.dart';
import 'package:doorcontrol/models/rest.dart';
import 'package:doorcontrol/services/api_service.dart';
import 'package:doorcontrol/screens/userlistscreen.dart';
import 'package:doorcontrol/screens/userdetailsscreen.dart';
import 'package:doorcontrol/screens/adduserscreen.dart';

import 'package:doorcontrol/routes.dart';

void main() {
  // runApp(VxState(store: DoorcontrolStore(), child: DoorcontrolApp()));

  runApp(DoorcontrolApp());
}

// class DoorcontrolStore extends VxStore {
//   final ApiService api = ApiService();
//   User? _selectedUser;
//   List<User> users = [];
// }

class DoorcontrolApp extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _DoorcontrolAppState();
}

class _DoorcontrolAppState extends State<DoorcontrolApp> {
  final ApiService api = ApiService();
  List<User> users = [];

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
            Routes.home: (uri, __) => MaterialPage(child: UsersListScreen()),
            Routes.adduser: (uri, __) => MaterialPage(child: AddUserScreen()),
            Routes.userdetails: (uri, __) {
              final String? user_id = uri.queryParameters["id"];
              return MaterialPage(child: UserDetailsScreen(user_id));
            }
          }),
    );
  }

  void loadList() {
    Future<List<User>> futureUsers = api.getUsers();
    futureUsers.then((usersList) {
      setState(() {
        this.users = usersList;
      });
    });
    // return futureUsers;
  }

  // void _handleUserTapped(User user) {
  //   setState(() {
  //     _selectedUser = user;
  //   });
  // }
}

//       title: 'Doorcontrol App',
//       home: Navigator(
//           pages: [
//             MaterialPage(
//               key: ValueKey('UsersListPage'),
//               child: UsersListScreen(
//                 users: users,
//                 onTapped: _handleUserTapped,
//               ),
//             ),
//             // if (_selectedUser != null) UserDetailsPage(user: _selectedUser)
//           ],
//           onPopPage: (route, result) {
//             if (!route.didPop(result)) {
//               return false;
//             }

//             // Update the list of pages by setting _selectedBook to null
//             loadList();
//             setState(() {
//               _selectedUser = null;
//             });

//             return true;
//           }),
//     );
//   }

//   void loadList() {
//     Future<List<User>> futureUsers = api.getUsers();
//     futureUsers.then((usersList) {
//       setState(() {
//         users = usersList;
//       });
//     });
//     // return futureUsers;
//   }

//   void _handleUserTapped(User user) {
//     setState(() {
//       _selectedUser = user;
//     });
//   }
// }

// class _MyHomePageState extends State<MyHomePage> {
//   final ApiService api = ApiService();
//   List<User> usersList = [];

//   @override
//   Widget build(BuildContext context) {
//     // This method is rerun every time setState is called, for instance as done
//     // by the _incrementCounter method above.
//     //
//     // The Flutter framework has been optimized to make rerunning build methods
//     // fast, so that you can just rebuild anything that needs updating rather
//     // than having to individually change instances of widgets.
//     return Scaffold(
//       appBar: AppBar(
//         // Here we take the value from the MyHomePage object that was created by
//         // the App.build method, and use it to set our appbar title.
//         title: Text(widget.title),
//       ),
//       body: new Container(
//         child: new Center(
//             child: new FutureBuilder(
//           future: loadList(),
//           builder: (context, snapshot) {
//             return usersList.length > 0
//                 ? new UserList(users: usersList)
//                 : new Center(
//                     child: new Text('No data found, tap plus button to add!',
//                         style: Theme.of(context).textTheme.title));
//           },
//         )),
//       ),
//       floatingActionButton: FloatingActionButton(
//         onPressed: () {
//           _navigateToAddScreen(context);
//         },
//         tooltip: 'Increment',
//         child: Icon(Icons.add),
//       ), // This trailing comma makes auto-formatting nicer for build methods.
//     );
//   }

//   Future loadList() {
//     Future<List<User>> futureUsers = api.getUsers();
//     futureUsers.then((usersList) {
//       setState(() {
//         this.usersList = usersList;
//       });
//     });
//     return futureUsers;
//   }

//   _navigateToAddScreen(BuildContext context) async {
//     final result = await Navigator.push(
//       context,
//       MaterialPageRoute(builder: (context) => AddDataWidget()),
//     );
//   }
// }
