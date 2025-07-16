import React, { useState } from 'react';
import { Box, Typography, Card, CardContent, IconButton, Grid } from '@mui/material';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import MoodBadIcon from '@mui/icons-material/MoodBad';
import DangerousIcon from '@mui/icons-material/Dangerous';
import DeleteIcon from '@mui/icons-material/Delete';

const mockAlerts = [
  {
    type: 'Theft',
    message: 'Theft detected in Zone A',
    time: '10:24 AM',
  },
  {
    type: 'Emotion',
    message: 'Angry person detected',
    time: '09:58 AM',
  },
  {
    type: 'Object',
    message: 'Knife detected',
    time: '09:45 AM',
  },
];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(mockAlerts);

  const handleDismiss = (idx) => {
    setAlerts(alerts.filter((_, i) => i !== idx));
  };

  return (
    <Box>
      <Typography variant="h4" color="secondary" gutterBottom>
        Alerts
      </Typography>
      <Grid container spacing={3}>
        {alerts.map((alert, idx) => (
          <Grid item xs={12} md={6} key={alert.message}>
            <Card sx={{ border: `2px solid ${alert.type === 'Theft' ? '#cfff04' : '#a259f7'}` }}>
              <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ mr: 2 }}>
                  {alert.type === 'Theft' ? (
                    <WarningAmberIcon sx={{ color: '#cfff04', fontSize: 40 }} />
                  ) : alert.type === 'Emotion' ? (
                    <MoodBadIcon sx={{ color: '#a259f7', fontSize: 40 }} />
                  ) : (
                    <DangerousIcon sx={{ color: '#a259f7', fontSize: 40 }} />
                  )}
                </Box>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="h6" color="secondary">
                    {alert.type}
                  </Typography>
                  <Typography color="primary" sx={{ fontWeight: 'bold' }}>
                    {alert.message}
                  </Typography>
                  <Typography color="secondary" sx={{ fontSize: 13 }}>
                    {alert.time}
                  </Typography>
                </Box>
                <IconButton onClick={() => handleDismiss(idx)}>
                  <DeleteIcon sx={{ color: '#cfff04' }} />
                </IconButton>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}