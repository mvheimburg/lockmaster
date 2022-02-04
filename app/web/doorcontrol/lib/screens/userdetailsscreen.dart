import 'package:flutter/material.dart';
// import 'dart:async';

import 'package:doorcontrol/models/rest.dart';
import 'package:doorcontrol/services/api_service.dart';

class UserDetailsScreen extends StatelessWidget {
  late final String? userId;
  Future<User>? _user;

  UserDetailsScreen(String? userId) {
    this.userId = userId;
    if (userId != null) {
      this._user = ApiService().getUserById(userId);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: FutureBuilder<User>(
          future: _user,
          builder: (BuildContext context, AsyncSnapshot<User> snapshot) {
            if (snapshot.hasData) {
              var user = snapshot.data!;
              return ListView(
                children: [
                  ListTile(
                    leading: Icon(Icons.person),
                    title: Text('Name'),
                    subtitle: Text(user.name),
                  ),
                  ListTile(
                    leading: Icon(Icons.person),
                    title: Text('Access level'),
                    subtitle: Text(user.accessLevel.toString()),
                  ),
                  ListTile(
                    leading: Icon(Icons.power),
                    title: Text('Pin'),
                    subtitle: Text(user.pin.toString()),
                  ),
                  ListTile(
                    leading: Icon(Icons.bluetooth),
                    title: Text('uuid'),
                    subtitle: Text(user.uuid.toString()),
                  ),
                  ListTile(
                    leading: Icon(Icons.lock_clock),
                    title: Text('Start'),
                    subtitle: Text(user.start.toString()),
                  ),
                  ListTile(
                    leading: Icon(Icons.lock_clock),
                    title: Text('End'),
                    subtitle: Text(user.end.toString()),
                  ),
                ],
              );
              // return Column(
              //   crossAxisAlignment: CrossAxisAlignment.start,
              //   children: [
              //     Text(snapshot.data!.name,
              //         style: Theme.of(context).textTheme.headline6),
              //     Text(snapshot.data!.pin.toString(),
              //         style: Theme.of(context).textTheme.subtitle1),
              //   ],
              // );
            } else if (snapshot.hasError) {
              return Text("${snapshot.error}");
            }
            return CircularProgressIndicator();
          },
        ),
      ),
    );
  }
}
