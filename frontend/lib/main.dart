// frontend/lib/main.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/auth_service.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';
import 'package:artisan_ai/services/api_service.dart';
import 'package:artisan_ai/theme/app_theme.dart';
import 'package:artisan_ai/screens/welcome_screen.dart';
import 'package:artisan_ai/screens/login_screen.dart';
import 'package:artisan_ai/screens/register_screen.dart';
import 'package:artisan_ai/screens/goal_definition_screen.dart';
import 'package:artisan_ai/screens/specify_output_screen.dart';
import 'package:artisan_ai/screens/provide_context_screen.dart';
import 'package:artisan_ai/screens/define_constraints_screen.dart';
import 'package:artisan_ai/screens/assign_persona_screen.dart';
import 'package:artisan_ai/screens/review_prompt_screen.dart';
import 'package:artisan_ai/screens/saved_configurations_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => AuthService()),
        // ApiService depends on AuthService. This ensures it gets the correct instance.
        ProxyProvider<AuthService, ApiService>(
          update: (context, authService, previousApiService) =>
              ApiService(authService),
        ),
        // PromptSessionService depends on ApiService.
        ChangeNotifierProvider(
          create: (context) => PromptSessionService(
            Provider.of<ApiService>(context, listen: false),
          ),
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
      title: 'Artisan AI',
      theme: AppTheme.darkTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const WelcomeScreen(),
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/goal': (context) => const GoalDefinitionScreen(),
        '/format': (context) => const SpecifyOutputScreen(),
        '/context': (context) => const ProvideContextScreen(),
        '/constraints': (context) => const DefineConstraintsScreen(),
        '/persona': (context) => const AssignPersonaScreen(),
        '/review': (context) => const ReviewPromptScreen(),
        '/saved': (context) => const SavedConfigurationsScreen(),
      },
    );
  }
}