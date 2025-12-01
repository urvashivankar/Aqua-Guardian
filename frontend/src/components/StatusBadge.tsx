import React from 'react';
import { Badge, BadgeProps } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

type StatusVariant = 'success' | 'warning' | 'danger' | 'info' | 'default';

const variantStyles: Record<StatusVariant, string> = {
  success: 'bg-success text-success-foreground',
  warning: 'bg-warning text-warning-foreground',
  danger: 'bg-destructive text-destructive-foreground',
  info: 'bg-ocean-primary text-primary-foreground',
  default: '',
};

interface StatusBadgeProps extends BadgeProps {
  status: string;
  variant?: StatusVariant;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, variant = 'default', className, ...props }) => {
  return (
    <Badge className={cn(variantStyles[variant], className)} {...props}>
      {status}
    </Badge>
  );
};

export default StatusBadge;

