// Path: frontend/lib/services/api_service.dart

import 'package:dio/dio.dart';
import 'auth_service.dart';

class ApiService {
  final Dio _dio = Dio();
  final AuthService _authService;
  static const String _baseUrl = 'http://127.0.0.1:8000/api/v1';

  ApiService(this._authService) {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _authService.getToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          options.baseUrl = _baseUrl;
          return handler.next(options);
        },
      ),
    );
  }

  // Handles GET requests
  Future<Response> get(String path) {
    return _dio.get(path);
  }

  // Handles POST requests with a JSON body
  Future<Response> post(String path, Map<String, dynamic> data) {
    return _dio.post(path, data: data);
  }

  // Handles POST requests with URL-encoded form data (for login)
  Future<Response> postUrlEncoded(String path, Map<String, dynamic> data) {
    return _dio.post(
      path,
      data: data,
      options: Options(contentType: Headers.formUrlEncodedContentType),
    );
  }
}