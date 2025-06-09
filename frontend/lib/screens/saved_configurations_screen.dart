// frontend/lib/screens/saved_configurations_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../services/prompt_session_service.dart';
import 'goal_definition_screen.dart';

class SavedConfigurationsScreen extends StatefulWidget {
  const SavedConfigurationsScreen({super.key});

  @override
  State<SavedConfigurationsScreen> createState() =>
      _SavedConfigurationsScreenState();
}

class _SavedConfigurationsScreenState extends State<SavedConfigurationsScreen> {
  late Future<List<dynamic>> _configurationsFuture;
  late final ApiService _apiService;

  @override
  void initState() {
    super.initState();
    _apiService = Provider.of<ApiService>(context, listen: false);
    _loadConfigurations();
  }

  void _loadConfigurations() {
    setState(() {
      _configurationsFuture = _apiService.getConfigurations();
    });
  }

  Future<void> _deleteConfiguration(int id) async {
    try {
      await _apiService.deleteConfiguration(id);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Configuration deleted successfully!')),
      );
      _loadConfigurations();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error deleting configuration: $e')),
      );
    }
  }

  void _loadConfigurationIntoSession(Map<String, dynamic> config) {
    final sessionService =
        Provider.of<PromptSessionService>(context, listen: false);
    sessionService.resetSession();
    sessionService.setGoal(config['goal'] ?? '');
    sessionService.setOutputFormat(config['output_format'] ?? '');
    sessionService.setContext(config['context']);
    sessionService.setConstraints(config['constraints']);
    sessionService.setPersona(
      description: config['persona_description'],
      skipped: config['persona_skipped'] ?? false,
    );

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const GoalDefinitionScreen()),
      (route) => route.isFirst,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Saved Configurations'),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _configurationsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text('No saved configurations found.'),
            );
          }

          final configurations = snapshot.data!;
          return ListView.builder(
            itemCount: configurations.length,
            itemBuilder: (context, index) {
              final config = configurations[index];
              return ListTile(
                title: Text(config['name'] ?? 'Untitled'),
                subtitle: Text(
                  config['goal'] ?? 'No goal specified.',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                onTap: () => _loadConfigurationIntoSession(config),
                trailing: IconButton(
                  icon: const Icon(Icons.delete, color: Colors.redAccent),
                  onPressed: () => _deleteConfiguration(config['id']),
                ),
              );
            },
          );
        },
      ),
    );
  }
}