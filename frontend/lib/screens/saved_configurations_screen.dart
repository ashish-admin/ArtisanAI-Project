// Path: frontend/lib/screens/saved_configurations_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class SavedConfigurationsScreen extends StatefulWidget {
  const SavedConfigurationsScreen({super.key});

  @override
  _SavedConfigurationsScreenState createState() =>
      _SavedConfigurationsScreenState();
}

class _SavedConfigurationsScreenState extends State<SavedConfigurationsScreen> {
  Future<List<dynamic>>? _savedSessionsFuture;

  @override
  void initState() {
    super.initState();
    // Fetch the sessions when the screen is first loaded
    _savedSessionsFuture = Provider.of<PromptSessionService>(context, listen: false).getSavedSessions();
  }

  @override
  Widget build(BuildContext context) {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Saved Configurations'),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _savedSessionsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No saved prompts found.'));
          }

          final configs = snapshot.data!;
          return ListView.builder(
            itemCount: configs.length,
            itemBuilder: (context, index) {
              final config = configs[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  leading: Icon(Icons.description_outlined, color: Theme.of(context).colorScheme.secondary),
                  title: Text(config['name'] ?? 'Untitled', style: Theme.of(context).textTheme.titleMedium),
                  subtitle: Text(config['description'] ?? '', maxLines: 1, overflow: TextOverflow.ellipsis,),
                  onTap: () {
                    // Populate the session service with the data from the saved config
                    sessionService.updateGoal(config['description'] ?? '');
                    sessionService.updateFormat(config['format'] ?? 'Text'); // Assuming format exists
                    sessionService.updateContext(config['original_text'] ?? '');
                    sessionService.updateConstraints(List<String>.from(config['constraints'] ?? []));
                    sessionService.updatePersona(config['persona'] ?? '');

                    // Navigate to the review screen to re-process or view the loaded prompt
                    Navigator.pushNamed(context, '/review');
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}