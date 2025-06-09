// Path: frontend/lib/widgets/educational_tooltip.dart

import 'package:flutter/material.dart';

class EducationalTooltip extends StatelessWidget {
  final String message;

  const EducationalTooltip({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: message,
      padding: const EdgeInsets.all(12),
      margin: const EdgeInsets.symmetric(horizontal: 24),
      textStyle: const TextStyle(fontSize: 14, color: Colors.white),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.8),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Icon(
        Icons.info_outline,
        size: 18,
        color: Colors.grey[400],
      ),
    );
  }
}