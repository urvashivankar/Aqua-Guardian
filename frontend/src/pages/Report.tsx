import React, { useState } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { MapPin, Send, AlertTriangle, CheckCircle, Eye, Filter } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/contexts/AuthContext';
import FileUploader from '@/components/FileUploader';
import ReportCard from '@/components/ReportCard';
import StatusBadge from '@/components/StatusBadge';
import { submitReport } from '@/services/api';

interface PollutionReport {
  id: string;
  location: string;
  type: string;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  description: string;
  reportedBy: string;
  date: string;
  status: 'Pending' | 'Investigating' | 'Resolved';
  image?: string;
}

const Report = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filter, setFilter] = useState('All');
  const [isGettingLocation, setIsGettingLocation] = useState(false);

  const [formData, setFormData] = useState({
    location: '',
    type: '',
    severity: 'Medium' as const,
    description: '',
    coordinates: '',
  });

  // Mock existing reports
  const [reports] = useState<PollutionReport[]>([
    {
      id: 'RPT001',
      location: 'Mumbai Harbor',
      type: 'Industrial Discharge',
      severity: 'Critical',
      description: 'Dark colored discharge observed from industrial facility',
      reportedBy: 'Environmental NGO',
      date: '2025-01-09',
      status: 'Investigating',
    },
    {
      id: 'RPT002',
      location: 'Ganges Delta',
      type: 'Plastic Pollution',
      severity: 'High',
      description: 'Large amounts of plastic waste accumulating near shore',
      reportedBy: 'Local Citizen',
      date: '2025-01-08',
      status: 'Pending',
    },
    {
      id: 'RPT003',
      location: 'Chennai Marina',
      type: 'Oil Spill',
      severity: 'Medium',
      description: 'Small oil spill detected near fishing boats',
      reportedBy: 'Fisherman Association',
      date: '2025-01-07',
      status: 'Resolved',
    },
    {
      id: 'RPT004',
      location: 'Kochi Backwaters',
      type: 'Sewage Overflow',
      severity: 'High',
      description: 'Untreated sewage flowing into backwater channels',
      reportedBy: 'Government Inspector',
      date: '2025-01-06',
      status: 'Investigating',
    },
  ]);

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      toast({
        title: "Geolocation Not Supported",
        description: "Your browser doesn't support geolocation",
        variant: "destructive",
      });
      return;
    }

    setIsGettingLocation(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude.toFixed(4);
        const lng = position.coords.longitude.toFixed(4);
        setFormData(prev => ({ ...prev, coordinates: `${lat}, ${lng}` }));
        setIsGettingLocation(false);
        toast({
          title: "Location Retrieved",
          description: `Coordinates: ${lat}, ${lng}`,
        });
      },
      (error) => {
        setIsGettingLocation(false);
        toast({
          title: "Location Error",
          description: "Could not retrieve your location. Please enter manually.",
          variant: "destructive",
        });
      }
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.location || !formData.type || !formData.description) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive",
      });
      return;
    }

    if (!selectedFile) {
      toast({
        title: "Missing Evidence",
        description: "Please upload a photo of the pollution",
        variant: "destructive",
      });
      return;
    }

    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please log in to submit a report",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      // Parse coordinates
      let lat = 0;
      let lng = 0;
      if (formData.coordinates) {
        const parts = formData.coordinates.split(',').map(p => parseFloat(p.trim()));
        if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
          lat = parts[0];
          lng = parts[1];
        }
      }

      // Map severity to integer
      const severityMap: Record<string, number> = {
        'Low': 1,
        'Medium': 5,
        'High': 8,
        'Critical': 10
      };

      const submitData = new FormData();
      submitData.append('user_id', user.id);
      submitData.append('latitude', lat.toString());
      submitData.append('longitude', lng.toString());
      submitData.append('description', `${formData.type} at ${formData.location}: ${formData.description}`);
      submitData.append('severity', (severityMap[formData.severity] || 5).toString());

      if (selectedFile) {
        submitData.append('file', selectedFile);
      }

      const responseData = await submitReport(submitData);

      // Backend returns the created report object
      const aiClass = responseData.ai_class;
      const aiConfidence = responseData.ai_confidence;

      if (aiClass && aiConfidence) {
        toast({
          title: "Report Verified by AI",
          description: `Detected: ${aiClass} (${(aiConfidence * 100).toFixed(1)}% confidence). Your report has been filed.`,
          variant: "default",
          className: "bg-green-50 border-green-200 text-green-800",
        });
      } else {
        toast({
          title: "Report Submitted Successfully!",
          description: "Your pollution report has been filed and is being reviewed",
        });
      }

      // Reset form
      setFormData({
        location: '',
        type: '',
        severity: 'Medium',
        description: '',
        coordinates: '',
      });

      setSelectedFile(null);
    } catch (error) {
      console.error('Error submitting report:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your report. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredReports = filter === 'All' ? reports : reports.filter(report => report.status === filter);

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <h1 className="text-3xl font-bold text-foreground">Pollution Reporting</h1>
        <p className="text-muted-foreground">
          Report water pollution incidents to help protect our ecosystems. Your reports make a difference.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Report Form */}
        <Card className="ocean-card">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              <span>Submit Pollution Report</span>
            </CardTitle>
            <CardDescription>
              Provide detailed information about the pollution incident you've observed
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="location" className="text-foreground">Location *</Label>
                  <Input
                    id="location"
                    placeholder="Enter specific location (e.g., Mumbai Harbor, Sector 5)"
                    value={formData.location}
                    onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                    className="mt-1 bg-background border-border focus:border-ocean-primary"
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="coordinates" className="text-foreground">GPS Coordinates (Optional)</Label>
                  <div className="flex space-x-2 mt-1">
                    <Input
                      id="coordinates"
                      placeholder="Latitude, Longitude"
                      value={formData.coordinates}
                      onChange={(e) => setFormData(prev => ({ ...prev, coordinates: e.target.value }))}
                      className="bg-background border-border focus:border-ocean-primary"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={getCurrentLocation}
                      disabled={isGettingLocation}
                    >
                      <MapPin className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div>
                  <Label htmlFor="type" className="text-foreground">Pollution Type *</Label>
                  <Select value={formData.type} onValueChange={(value) => setFormData(prev => ({ ...prev, type: value }))}>
                    <SelectTrigger className="mt-1 bg-background border-border focus:border-ocean-primary">
                      <SelectValue placeholder="Select pollution type" />
                    </SelectTrigger>
                    <SelectContent className="ocean-card border-border">
                      <SelectItem value="Industrial Discharge">Industrial Discharge</SelectItem>
                      <SelectItem value="Plastic Pollution">Plastic Pollution</SelectItem>
                      <SelectItem value="Oil Spill">Oil Spill</SelectItem>
                      <SelectItem value="Sewage Overflow">Sewage Overflow</SelectItem>
                      <SelectItem value="Chemical Contamination">Chemical Contamination</SelectItem>
                      <SelectItem value="Agricultural Runoff">Agricultural Runoff</SelectItem>
                      <SelectItem value="Other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="severity" className="text-foreground">Severity Level</Label>
                  <Select value={formData.severity} onValueChange={(value: any) => setFormData(prev => ({ ...prev, severity: value }))}>
                    <SelectTrigger className="mt-1 bg-background border-border focus:border-ocean-primary">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="ocean-card border-border">
                      <SelectItem value="Low">Low - Minor Impact</SelectItem>
                      <SelectItem value="Medium">Medium - Moderate Impact</SelectItem>
                      <SelectItem value="High">High - Significant Impact</SelectItem>
                      <SelectItem value="Critical">Critical - Immediate Action Required</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="description" className="text-foreground">Description *</Label>
                  <Textarea
                    id="description"
                    placeholder="Provide detailed description of what you observed, including time, weather conditions, and any other relevant information..."
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                    className="mt-1 min-h-[100px] bg-background border-border focus:border-ocean-primary"
                    required
                  />
                </div>

                <div>
                  <Label className="text-foreground">Photo Evidence *</Label>
                  <FileUploader onFileSelect={setSelectedFile} />
                  {selectedFile && (
                    <p className="text-xs text-muted-foreground mt-1">
                      Selected file: {selectedFile.name}
                    </p>
                  )}
                </div>
              </div>

              <Button
                type="submit"
                className="w-full wave-animation"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  "Submitting Report..."
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Submit Report
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Guidelines */}
        <Card className="ocean-card">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-success" />
              <span>Reporting Guidelines</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <h4 className="font-semibold text-foreground">What to Include:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-ocean-primary rounded-full mt-2 flex-shrink-0"></div>
                  <span>Exact location with landmarks</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-ocean-primary rounded-full mt-2 flex-shrink-0"></div>
                  <span>Date and time of observation</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-ocean-primary rounded-full mt-2 flex-shrink-0"></div>
                  <span>Clear photos or videos if possible</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-ocean-primary rounded-full mt-2 flex-shrink-0"></div>
                  <span>Weather conditions</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-ocean-primary rounded-full mt-2 flex-shrink-0"></div>
                  <span>Suspected source if known</span>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-foreground">Safety First:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-warning rounded-full mt-2 flex-shrink-0"></div>
                  <span>Do not touch contaminated water</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-warning rounded-full mt-2 flex-shrink-0"></div>
                  <span>Avoid inhaling fumes or vapors</span>
                </li>
                <li className="flex items-start space-x-2">
                  <div className="w-1.5 h-1.5 bg-warning rounded-full mt-2 flex-shrink-0"></div>
                  <span>Report from a safe distance</span>
                </li>
              </ul>
            </div>

            <div className="bg-card/50 p-4 rounded-lg border border-border">
              <h5 className="font-medium text-foreground mb-2">Emergency Situations</h5>
              <p className="text-sm text-muted-foreground">
                For immediate threats to human health or environment, also contact local authorities:
                <span className="block mt-1 font-medium text-ocean-primary">Emergency: 112</span>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Featured Reports */}
      <Card className="ocean-card">
        <CardHeader>
          <CardTitle>Featured Field Reports</CardTitle>
          <CardDescription>Highlights sourced from the latest submissions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {reports.slice(0, 2).map((report) => (
              <ReportCard key={report.id} {...report} />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Submitted Reports */}
      <Card className="ocean-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Eye className="h-5 w-5 text-ocean-primary" />
                <span>Recent Reports</span>
              </CardTitle>
              <CardDescription>
                Track submitted pollution reports and their status
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <Select value={filter} onValueChange={setFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="All">All Reports</SelectItem>
                  <SelectItem value="Pending">Pending</SelectItem>
                  <SelectItem value="Investigating">Investigating</SelectItem>
                  <SelectItem value="Resolved">Resolved</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Report ID</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Severity</TableHead>
                  <TableHead>Reported By</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredReports.map((report) => (
                  <TableRow key={report.id}>
                    <TableCell className="font-medium">{report.id}</TableCell>
                    <TableCell>{report.location}</TableCell>
                    <TableCell>{report.type}</TableCell>
                    <TableCell>
                      <StatusBadge
                        status={report.severity}
                        variant={
                          report.severity === 'Critical'
                            ? 'danger'
                            : report.severity === 'High'
                              ? 'warning'
                              : report.severity === 'Medium'
                                ? 'info'
                                : 'success'
                        }
                      />
                    </TableCell>
                    <TableCell>{report.reportedBy}</TableCell>
                    <TableCell>{report.date}</TableCell>
                    <TableCell>
                      <StatusBadge
                        status={report.status}
                        variant={
                          report.status === 'Resolved'
                            ? 'success'
                            : report.status === 'Investigating'
                              ? 'info'
                              : 'warning'
                        }
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Report;