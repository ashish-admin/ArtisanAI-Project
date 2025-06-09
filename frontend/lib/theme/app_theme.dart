// frontend/lib/theme/app_theme.dart

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static final ThemeData darkTheme = ThemeData(
    brightness: Brightness.dark,
    primaryColor: const Color(0xFF0D1B2A),
    scaffoldBackgroundColor: const Color(0xFF0D1B2A),
    appBarTheme: AppBarTheme(
      color: const Color(0xFF1B263B),
      elevation: 0,
      titleTextStyle: GoogleFonts.lato(
        color: const Color(0xFFE0E1DD),
        fontSize: 20,
        fontWeight: FontWeight.bold,
      ),
    ),
    colorScheme: const ColorScheme.dark(
      primary: Color(0xFF3A7CA5),
      secondary: Color(0xFF81B2D9),
      background: Color(0xFF0D1B2A),
      surface: Color(0xFF1B263B),
      onPrimary: Colors.white,
      onSecondary: Colors.white,
      onBackground: Color(0xFFE0E1DD),
      onSurface: Color(0xFFE0E1DD),
      error: Color(0xFFD9534F),
      onError: Colors.white,
    ),
    textTheme: TextTheme(
      displayLarge: GoogleFonts.robotoCondensed(fontSize: 96, fontWeight: FontWeight.bold, color: const Color(0xFFE0E1DD)),
      displayMedium: GoogleFonts.robotoCondensed(fontSize: 60, fontWeight: FontWeight.bold, color: const Color(0xFFE0E1DD)),
      displaySmall: GoogleFonts.robotoCondensed(fontSize: 48, fontWeight: FontWeight.bold, color: const Color(0xFFE0E1DD)),
      headlineMedium: GoogleFonts.lato(fontSize: 34, fontWeight: FontWeight.normal, color: const Color(0xFFE0E1DD)),
      headlineSmall: GoogleFonts.lato(fontSize: 24, fontWeight: FontWeight.normal, color: const Color(0xFFE0E1DD)),
      titleLarge: GoogleFonts.lato(fontSize: 20, fontWeight: FontWeight.w500, color: const Color(0xFFE0E1DD)),
      bodyLarge: GoogleFonts.lato(fontSize: 16, fontWeight: FontWeight.normal, color: const Color(0xFFE0E1DD)),
      bodyMedium: GoogleFonts.lato(fontSize: 14, fontWeight: FontWeight.normal, color: const Color(0xFFE0E1DD)),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: const Color(0xFF3A7CA5),
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
        textStyle: GoogleFonts.lato(fontSize: 16, fontWeight: FontWeight.bold),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
      filled: true,
      fillColor: Color(0xFF1B263B),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.all(Radius.circular(8)),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.all(Radius.circular(8)),
        borderSide: BorderSide(color: Color(0xFF3A7CA5)),
      ),
    ),
  );
}