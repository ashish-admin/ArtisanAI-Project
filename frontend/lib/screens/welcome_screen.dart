// Path: frontend/lib/screens/welcome_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/auth_service.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  _WelcomeScreenState createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {
  @override
  void initState() {
    super.initState();
    // Use addPostFrameCallback to ensure the context is available
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkLoginStatus();
    });
  }

  Future<void> _checkLoginStatus() async {
    final authService = Provider.of<AuthService>(context, listen: false);
    await authService.tryAutoLogin();
    if (mounted && authService.isAuthenticated) {
      Navigator.of(context).pushReplacementNamed('/creation_hub');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              const Icon(
                Icons.hub_outlined, // Icon suggesting connection/intelligence
                size: 80,
                color: Color(0xFF81B2D9),
              ),
              const SizedBox(height: 24),
              Text(
                'Synaptiq.ai',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.displaySmall?.copyWith(
                      color: Colors.white,
                    ),
              ),
              const SizedBox(height: 12),
              Text(
                'Your Intelligent Prompt Co-Pilot',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Colors.white70,
                    ),
              ),
              const SizedBox(height: 64),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/login');
                },
                child: const Text('Login'),
              ),
              const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/register');
                },
                style: OutlinedButton.styleFrom(
                  side: BorderSide(color: Theme.of(context).colorScheme.primary),
                  padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  textStyle: Theme.of(context).elevatedButtonTheme.style?.textStyle?.resolve({}),
                ),
                child: const Text('Register'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}