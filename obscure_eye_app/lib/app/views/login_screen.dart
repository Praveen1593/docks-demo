import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import '../routes/app_routes.dart';
import '../theme/cyberpunk_theme.dart';

class LoginScreen extends StatelessWidget {
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: black,
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 32.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SvgPicture.asset(
                  'assets/obscure_eye_logo.svg',
                  width: 100,
                  height: 80,
                ),
                SizedBox(height: 24),
                Text(
                  'Welcome Back',
                  style: TextStyle(
                    color: neonLime,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 32),
                TextField(
                  controller: usernameController,
                  style: TextStyle(color: neonLime),
                  decoration: InputDecoration(
                    labelText: 'Username',
                    labelStyle: TextStyle(color: neonPurple),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: neonPurple),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: neonLime),
                    ),
                  ),
                ),
                SizedBox(height: 20),
                TextField(
                  controller: passwordController,
                  obscureText: true,
                  style: TextStyle(color: neonLime),
                  decoration: InputDecoration(
                    labelText: 'Password',
                    labelStyle: TextStyle(color: neonPurple),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: neonPurple),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: neonLime),
                    ),
                  ),
                ),
                SizedBox(height: 32),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: neonPurple,
                      onPrimary: black,
                      padding: EdgeInsets.symmetric(vertical: 16),
                      textStyle: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    onPressed: () {
                      // Mock login, go to main screen
                      Get.offAllNamed(Routes.MAIN);
                    },
                    child: Text('Login'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}