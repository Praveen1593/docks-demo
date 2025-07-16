import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import VideocamIcon from '@mui/icons-material/Videocam';

export default function LivePage() {
  return (
    <Box>
      <Typography variant="h4" color="secondary" gutterBottom>
        Live View
      </Typography>
      <Card sx={{ maxWidth: 480, margin: '32px auto', background: '#2d0036', border: '2px solid #cfff04' }}>
        <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 6 }}>
          <VideocamIcon sx={{ fontSize: 80, color: '#a259f7' }} />
          <Typography variant="h6" color="secondary" sx={{ mt: 2 }}>
            Live camera feed (mock)
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}