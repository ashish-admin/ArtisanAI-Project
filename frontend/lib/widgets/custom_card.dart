// Path: frontend/lib/widgets/custom_card.dart

import 'package:flutter/material.dart';

class CustomCard extends StatelessWidget {
  final String title;
  final Widget child;
  final Widget? action; // Action for the top-right corner
  final Widget? titleAction; // Action widget next to the title

  const CustomCard({
    super.key,
    required this.title,
    required this.child,
    this.action,
    this.titleAction,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      color: theme.colorScheme.surface.withOpacity(0.5),
      elevation: 0,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: theme.dividerColor, width: 0.5),
        borderRadius: BorderRadius.circular(12.0),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Row(
                    children: [
                      Text(
                        title,
                        style: theme.textTheme.titleLarge?.copyWith(
                          color: theme.colorScheme.secondary,
                        ),
                      ),
                      if (titleAction != null) ...[
                        const SizedBox(width: 8),
                        titleAction!,
                      ]
                    ],
                  ),
                ),
                if (action != null) action!,
              ],
            ),
            const Divider(height: 24),
            child,
          ],
        ),
      ),
    );
  }
}