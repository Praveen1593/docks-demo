import React from 'react';
import { Box, Typography, Card, CardContent, Switch, Button } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';

export default function SettingsPage() {
  return (
    <Box>
      <Typography variant="h4" color="secondary" gutterBottom>
        Settings
      </Typography>
      <Card sx={{ maxWidth: 480, margin: '32px auto', background: '#2d0036', border: '2px solid #a259f7' }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <AccountCircleIcon sx={{ color: '#cfff04', fontSize: 40, mr: 2 }} />
            <Box>
              <Typography color="secondary" fontWeight="bold">Admin User</Typography>
              <Typography color="primary">admin@obscureeye.ai</Typography>
            </Box>
          </Box>
          <Box display="flex" alignItems="center" mb={2}>
            <Typography color="secondary" fontWeight="bold" mr={2}>Dark Mode</Typography>
            <Switch checked disabled sx={{ color: '#cfff04' }} />
          </Box>
          <Button variant="contained" color="primary" startIcon={<LogoutIcon />} fullWidth>
            Logout
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}