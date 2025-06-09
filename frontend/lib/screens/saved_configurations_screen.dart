// frontend/lib/screens/saved_configurations_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class SavedConfigurationsScreen extends StatelessWidget {
  const SavedConfigurationsScreen({super.key});

  // Dummy data for saved configurations
  final List<Map<String, dynamic>> savedConfigs = const [
    {
      "name": "Novel Chapter Critique",
      "goal": "Critique the pacing and dialogue of my first chapter.",
      "output_format": "Detailed feedback with suggestions.",
      "context": "The wind howled outside the small cottage...",
      "constraints": ["under 1000 words"],
      "persona": "A seasoned book editor"
    },
    {
      "name": "Email to Manager",
      "goal": "Write a professional email requesting a project extension.",
      "output_format": "Polite and concise email.",
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
          return ListTile(
            title: Text(config['name']),
            subtitle: Text(config['goal']),
            onTap: () {
              // Corrected to use 'update' methods
              sessionService.updateGoal(config['goal'] ?? '');
              sessionService.updateFormat(config['output_format'] ?? '');
              sessionService.updateContext(config['context'] ?? '');
              sessionService.updateConstraints(List<String>.from(config['constraints'] ?? []));
              sessionService.updatePersona(config['persona'] ?? '');

              // Navigate to the review screen to process the loaded configuration
              Navigator.pushNamed(context, '/review');
            },
          );
        },
      ),
    );
  }
}