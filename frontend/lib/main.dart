// frontend/lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/login_screen.dart';
import 'screens/welcome_screen.dart';
import 'services/api_service.dart';
import 'services/auth_service.dart';
import 'services/prompt_session_service.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthService()),
        ChangeNotifierProvider(create: (_) => PromptSessionService()),
        ProxyProvider<AuthService, ApiService>(
          update: (context, authService, previousApiService) =>
              ApiService(authService),
        ),
      ],
      child: MaterialApp(
        title: 'ArtisanAI',
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        home: const AuthCheck(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}

class AuthCheck extends StatelessWidget {
  const AuthCheck({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      // This Future runs only once when AuthCheck is first built.
      future: Provider.of<AuthService>(context, listen: false).tryAutoLogin(),
      builder: (context, authResultSnapshot) {
        // While waiting for tryAutoLogin to complete, show a loading indicator.
        if (authResultSnapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }

        // After the Future completes, use a Consumer to listen for auth changes.
        return Consumer<AuthService>(
          builder: (context, authService, child) {
            // Use the synchronous getter to decide which screen to show.
            return authService.isAuthenticated
                ? const WelcomeScreen()
                : const LoginScreen();
          },
        );
      },
    );
  }
}