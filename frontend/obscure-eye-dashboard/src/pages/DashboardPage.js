import React from 'react';
import { Box, Typography, Card, CardContent, Grid, Button } from '@mui/material';
import VideocamIcon from '@mui/icons-material/Videocam';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import SettingsIcon from '@mui/icons-material/Settings';

export default function DashboardPage() {
  return (
    <Box>
      <Typography variant="h4" color="secondary" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="secondary">Active Cameras</Typography>
              <Typography variant="h3" color="primary">4</Typography>
              <VideocamIcon color="secondary" sx={{ fontSize: 40 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="secondary">Alerts Today</Typography>
              <Typography variant="h3" color="primary">12</Typography>
              <WarningAmberIcon color="secondary" sx={{ fontSize: 40 }} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Box mt={5}>
        <Typography variant="h6" color="secondary" gutterBottom>
          Quick Links
        </Typography>
        <Grid container spacing={2}>
          <Grid item>
            <Button variant="contained" color="secondary" startIcon={<VideocamIcon />} href="/live">
              Live View
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" startIcon={<WarningAmberIcon />} href="/alerts">
              Alerts
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="secondary" startIcon={<SettingsIcon />} href="/settings">
              Settings
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}