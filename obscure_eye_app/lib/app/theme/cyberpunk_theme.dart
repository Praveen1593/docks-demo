import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

final Color darkPurple = Color(0xFF2d0036);
final Color neonPurple = Color(0xFFa259f7);
final Color neonLime = Color(0xFFcfff04);
final Color black = Color(0xFF181818);
final Color white = Color(0xFFFFFFFF);

final ThemeData cyberpunkTheme = ThemeData(
  brightness: Brightness.dark,
  primaryColor: neonPurple,
  accentColor: neonLime,
  scaffoldBackgroundColor: black,
  appBarTheme: AppBarTheme(
    color: darkPurple,
    iconTheme: IconThemeData(color: neonLime),
    titleTextStyle: GoogleFonts.orbitron(
      color: neonLime,
      fontSize: 22,
      fontWeight: FontWeight.bold,
      letterSpacing: 2,
    ),
  ),
  textTheme: GoogleFonts.orbitronTextTheme().apply(
    bodyColor: white,
    displayColor: neonLime,
  ),
  floatingActionButtonTheme: FloatingActionButtonThemeData(
    backgroundColor: neonPurple,
    foregroundColor: black,
  ),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    backgroundColor: darkPurple,
    selectedItemColor: neonLime,
    unselectedItemColor: neonPurple,
    selectedLabelStyle: GoogleFonts.orbitron(fontWeight: FontWeight.bold),
    unselectedLabelStyle: GoogleFonts.orbitron(),
  ),
  cardColor: darkPurple,
  iconTheme: IconThemeData(color: neonLime),
  buttonTheme: ButtonThemeData(
    buttonColor: neonPurple,
    textTheme: ButtonTextTheme.primary,
  ),
);