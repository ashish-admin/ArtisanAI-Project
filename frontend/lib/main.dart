// Path: frontend/lib/main.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/auth_service.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';
import 'package:artisan_ai/services/api_service.dart';
import 'package:artisan_ai/theme/app_theme.dart';
import 'package:artisan_ai/screens/welcome_screen.dart';
import 'package:artisan_ai/screens/login_screen.dart';
import 'package:artisan_ai/screens/register_screen.dart';
import 'package:artisan_ai/screens/creation_hub_screen.dart';
import 'package:artisan_ai/screens/review_prompt_screen.dart';
import 'package:artisan_ai/screens/saved_configurations_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        // 1. AuthService is created once and provided to the whole app.
        ChangeNotifierProvider(create: (context) => AuthService()),

        // 2. ApiService is created and is given the AuthService instance.
        //    It will update whenever AuthService changes.
        ProxyProvider<AuthService, ApiService>(
          update: (context, authService, previousApiService) =>
              ApiService(authService),
        ),

        // 3. PromptSessionService is created and given the ApiService instance.
        ChangeNotifierProxyProvider<ApiService, PromptSessionService>(
          create: (context) => PromptSessionService(
            Provider.of<ApiService>(context, listen: false),
          ),
          update: (context, apiService, previousSessionService) =>
              PromptSessionService(apiService),
        ),
      ],
      child: const ArtisanAI(),
    ),
  );
}

class ArtisanAI extends StatelessWidget {
  const ArtisanAI({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Synaptiq.ai',
      theme: AppTheme.darkTheme,
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => const WelcomeScreen(),
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/creation_hub': (context) => const CreationHubScreen(),
        '/review': (context) => const ReviewPromptScreen(),
        '/saved': (context) => const SavedConfigurationsScreen(),
      },
    );
  }
}