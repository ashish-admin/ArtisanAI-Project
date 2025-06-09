// frontend/lib/screens/welcome_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../services/prompt_session_service.dart';
import 'login_screen.dart';
import 'goal_definition_screen.dart';
import 'saved_configurations_screen.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  void _startNewCoPilot(BuildContext context) {
    // Correctly reset the session state using the new method name.
    Provider.of<PromptSessionService>(context, listen: false).resetSession();
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const GoalDefinitionScreen(),
      ),
    );
  }

  void _loadConfigurations(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const SavedConfigurationsScreen(),
      ),
    );
  }

  void _logout(BuildContext context) {
    final authService = Provider.of<AuthService>(context, listen: false);
    authService.logout();
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Welcome to ArtisanAI'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => _logout(context),
            tooltip: 'Logout',
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'ArtisanAI Co-Pilot',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Start New Prompt'),
              onPressed: () => _startNewCoPilot(context),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                textStyle: const TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 20),
            TextButton.icon(
              icon: const Icon(Icons.history),
              label: const Text('Load Saved Configuration'),
              onPressed: () => _loadConfigurations(context),
            ),
          ],
        ),
      ),
    );
  }
}