import 'dart:convert';
import 'dart:io';

import 'package:doorcontrol/models/rest.dart';
import 'package:http/http.dart' as http;

class ApiService {
  // final String apiUrl = "/doormanager";
  // final String buildType = 'dev';
  final String buildType = 'staging';
  late final String apiUrl;
  //
  // ApiService._(this.buildType, this.apiUrl);

  ApiService() {
    if (buildType == 'staging') {
      apiUrl = "/doormanager";
    } else {
      apiUrl = "http://localhost:5555";
    }
  }
  //   return new ApiService._();
  // }

  Future<List<User>> getUsers() async {
    final http.Response response =
        await http.get(Uri.parse("$apiUrl/get_users"));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      List<User> users =
          body.map((dynamic item) => User.fromJson(item)).toList();
      return users;
    } else {
      throw "Failed to load User list";
    }
  }

  Future<List<Candidate>> getCandidates() async {
    final http.Response response =
        await http.get(Uri.parse("$apiUrl/get_current_candidate_list"));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      List<Candidate> candidates =
          body.map((dynamic item) => Candidate.fromJson(item)).toList();
      return candidates;
    } else {
      throw "Failed to load User list";
    }
  }

  Future<User> getUserById(String id) async {
    http.Response response = await http.get(Uri.parse("$apiUrl/get_user/$id"));

    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load a user');
    }
  }

  Future<User> createUser(User user) async {
    Map data = {
      'name': user.name,
      'pin': user.pin,
      'mac': user.mac,
      'end': user.end,
      'access_level': user.accessLevel
    };

    http.Response response = await http.post(
      Uri.parse("$apiUrl/create_user"),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 201) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to post User');
    }
  }

  Future<User> updateUser(String id, User user) async {
    Map data = {
      'name': user.name,
      'pin': user.pin,
      'mac': user.mac,
      'end': user.end,
      'access_level': user.accessLevel
    };

    http.Response response = await http.put(
      Uri.parse("$apiUrl/get_user/$id"),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to update a user');
    }
  }

  Future<void> deleteUser(String id) async {
    http.Response res = await http.delete(Uri.parse("$apiUrl/delete_user/$id"));

    if (res.statusCode == 200) {
      print("User deleted");
    } else {
      throw "Failed to delete a user.";
    }
  }
}
