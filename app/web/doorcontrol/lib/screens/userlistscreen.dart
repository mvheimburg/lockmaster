import 'package:flutter/material.dart';
import "package:velocity_x/velocity_x.dart";

import 'package:doorcontrol/models/rest.dart';
import 'package:doorcontrol/screens/userlistscreen.dart';
import 'package:doorcontrol/routes.dart';
import 'package:doorcontrol/services/api_service.dart';

import 'package:doorcontrol/models/rest.dart';

class UsersListScreen extends StatelessWidget {
  final ApiService api = ApiService();
  late Future<List<User>> _users;

  UsersListScreen() {
    this._users = this.api.getUsers();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: FutureBuilder<List<User>>(
        future: _users,
        builder: (BuildContext context, AsyncSnapshot<List<User>> snapshot) {
          if (snapshot.hasData) {
            var users = snapshot.data!;
            return ListView(
              children: [
                for (var user in users) ...[
                  ListTile(
                    leading: Icon(Icons.person),
                    title: Text(user.name.toString()),
                    subtitle: Text(user.accessLevel.toString()),
                    // subtitle: Text(user.mac.toString()),
                    onTap: () => context.vxNav.push(
                        Uri(
                            path: Routes.userdetails,
                            queryParameters: {"id": user.id.toString()}),
                        params: user),
                  )
                ],
              ],
            );
          } else if (snapshot.hasError) {
            return Text("${snapshot.error}");
          }
          return CircularProgressIndicator();
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.vxNav.push(
          Uri(path: Routes.adduser),
        ),
      ),
    );
  }
}
