// frontend/test/widget_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/main.dart'; // This correctly imports ArtisanAI

// Mock or real services needed for the test
import 'package:artisan_ai/services/auth_service.dart';
import 'package:artisan_ai/services/api_service.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

void main() {
  testWidgets('Renders WelcomeScreen on initial load', (WidgetTester tester) async {
    // Build our app with all the necessary providers and trigger a frame.
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (context) => AuthService()),
          ProxyProvider<AuthService, ApiService>(
            update: (context, authService, previousApiService) =>
                ApiService(authService),
          ),
          ChangeNotifierProvider(
            create: (context) => PromptSessionService(
              Provider.of<ApiService>(context, listen: false),
            ),
          ),
        ],
        // The child is your actual app widget
        child: const ArtisanAI(), // Corrected name: ArtisanAI
      ),
    );

    // Now, you can write a meaningful test. For example, let's verify
    // the WelcomeScreen is shown, since it's your initial route.
    expect(find.text('Welcome to Artisan AI'), findsOneWidget); // Adjust text if it's different
    expect(find.text('Login'), findsOneWidget);
    expect(find.text('Register'), findsOneWidget);
  });
}