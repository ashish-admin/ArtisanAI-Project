// Path: frontend/lib/screens/saved_configurations_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class SavedConfigurationsScreen extends StatelessWidget {
  const SavedConfigurationsScreen({super.key});

  // Dummy data for demonstration
  final List<Map<String, dynamic>> savedConfigs = const [
    {
      "name": "Novel Chapter Critique",
      "goal": "Critique the pacing and dialogue of my first chapter.",
      "format": "Detailed feedback with suggestions.",
      "context": "The wind howled outside the small cottage...",
      "constraints": ["under 1000 words"],
      "persona": "A seasoned book editor"
    },
    {
      "name": "Email to Manager",
      "goal": "Write a professional email requesting a project extension.",
      "format": "Email",
      "context": "Project deadline is this Friday, need one more week.",
      "constraints": ["formal tone"],
      "persona": "An efficient project manager"
    }
  ];

  @override
  Widget build(BuildContext context) {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Saved Configurations'),
      ),
      body: ListView.builder(
        itemCount: savedConfigs.length,
        itemBuilder: (context, index) {
          final config = savedConfigs[index];
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ListTile(
              title: Text(config['name'], style: Theme.of(context).textTheme.titleMedium),
              subtitle: Text(config['goal']),
              onTap: () {
                sessionService.updateGoal(config['goal'] ?? '');
                sessionService.updateFormat(config['format'] ?? 'Text');
                sessionService.updateContext(config['context'] ?? '');
                sessionService.updateConstraints(List<String>.from(config['constraints'] ?? []));
                sessionService.updatePersona(config['persona'] ?? '');

                Navigator.pushNamed(context, '/review');
              },
            ),
          );
        },
      ),
    );
  }
}