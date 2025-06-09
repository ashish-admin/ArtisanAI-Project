// frontend/lib/services/auth_service.dart

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService with ChangeNotifier {
  final String _baseUrl = 'http://127.0.0.1:8000';
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  String? _token;

  bool get isAuthenticated => _token != null;

  Future<void> tryAutoLogin() async {
    _token = await _storage.read(key: 'auth_token');
    if (_token != null) {
      notifyListeners();
    }
  }

  Future<String?> getToken() async {
    if (_token != null) return _token;
    _token = await _storage.read(key: 'auth_token');
    return _token;
  }

  Future<bool> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/api/v1/auth/token'),
      headers: <String, String>{
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'username': email, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final tokenFromServer = data['access_token'];
      if (tokenFromServer != null) {
        await _saveToken(tokenFromServer);
        notifyListeners();
        return true;
      }
    }
    return false;
  }

  Future<bool> register(String email, String password) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/api/v1/auth/register'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{'email': email, 'password': password}),
    );
    return response.statusCode == 201;
  }

  Future<void> logout() async {
    _token = null;
    await _storage.delete(key: 'auth_token');
    notifyListeners();
  }

  Future<void> _saveToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
    _token = token;
  }
}