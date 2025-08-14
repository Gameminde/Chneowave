/**
 * 🔍 Composants Accessibles WCAG 2.1 - Phase 3.1
 * Selon prompt ultra-précis : composants conformes AA/AAA
 * 
 * Remplacements accessibles pour les composants critiques CHNeoWave
 */

import React, { forwardRef, useRef, useEffect, useState } from 'react';
import { 
  useFocusTrap, 
  useKeyboardFocusVisible,
  generateAriaId,
  getFieldAriaProps,
  getStatusAriaProps,
  getLoadingAriaProps,
  TARGET_SIZE_CLASSES,
  ErrorMessages,
  SuccessMessages
} from '../utils/AccessibilityHelpers';

// ============ BOUTON ACCESSIBLE ============

interface AccessibleButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  loadingText?: string;
  children: React.ReactNode;
}

export const AccessibleButton = forwardRef<HTMLButtonElement, AccessibleButtonProps>(({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  loadingText = 'Chargement...',
  children,
  disabled,
  className = '',
  ...props
}, ref) => {
  const baseClasses = `
    ${TARGET_SIZE_CLASSES.button}
    inline-flex items-center justify-center
    font-medium rounded-lg transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    touch-manipulation
  `;

  const variantClasses = {
    primary: 'bg-[var(--accent-primary)] text-[var(--text-inverse)] hover:bg-[var(--accent-primary-hover)] focus:ring-[var(--accent-primary)]',
    secondary: 'bg-[var(--bg-secondary)] text-[var(--text-secondary)] border border-[var(--border-primary)] hover:bg-[var(--bg-tertiary)] focus:ring-[var(--accent-primary)]',
    danger: 'bg-[var(--status-error)] text-[var(--text-inverse)] hover:opacity-90 focus:ring-[var(--status-error)]',
    success: 'bg-[var(--status-success)] text-[var(--text-inverse)] hover:opacity-90 focus:ring-[var(--status-success)]'
  };

  const sizeClasses = {
    sm: 'text-sm px-3 py-2 min-h-[40px]',
    md: 'text-sm px-4 py-2 min-h-[44px]',
    lg: 'text-base px-6 py-3 min-h-[48px]'
  };

  const loadingProps = getLoadingAriaProps(isLoading, loadingText);

  return (
    <button
      ref={ref}
      disabled={disabled || isLoading}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...loadingProps}
      {...props}
    >
      {isLoading && (
        <svg 
          className="w-4 h-4 mr-2 animate-spin" 
          fill="none" 
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4" 
            className="opacity-25"
          />
          <path 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            className="opacity-75"
          />
        </svg>
      )}
      <span className={isLoading ? 'sr-only' : ''}>{children}</span>
      {isLoading && <span className="ml-2">{loadingText}</span>}
    </button>
  );
});

AccessibleButton.displayName = 'AccessibleButton';

// ============ CHAMP DE FORMULAIRE ACCESSIBLE ============

interface AccessibleInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  description?: string;
  showLabel?: boolean;
}

export const AccessibleInput = forwardRef<HTMLInputElement, AccessibleInputProps>(({
  label,
  error,
  description,
  showLabel = true,
  required = false,
  className = '',
  id: providedId,
  ...props
}, ref) => {
  const id = providedId || generateAriaId('input');
  const descriptionId = `${id}-description`;
  const errorId = `${id}-error`;

  const fieldProps = getFieldAriaProps(id, label, error, description, required);

  return (
    <div className="space-y-2">
      {showLabel && (
        <label 
          htmlFor={id}
          className="block text-sm font-medium text-[var(--text-secondary)]"
        >
          {label}
          {required && <span className="text-[var(--status-error)] ml-1" aria-label="obligatoire">*</span>}
        </label>
      )}
      
      {description && (
        <p 
          id={descriptionId}
          className="text-sm text-[var(--text-muted)]"
        >
          {description}
        </p>
      )}
      
      <input
        ref={ref}
        className={`
          ${TARGET_SIZE_CLASSES.input}
          w-full bg-[var(--bg-input)] text-[var(--text-primary)]
          border border-[var(--border-primary)] rounded-lg
          focus:outline-none focus:ring-2 focus:ring-[var(--accent-primary)]
          focus:border-[var(--border-focus)]
          disabled:bg-[var(--bg-disabled)] disabled:cursor-not-allowed
          placeholder:text-[var(--text-muted)]
          transition-all duration-200
          ${error ? 'border-[var(--status-error)] focus:ring-[var(--status-error)]' : ''}
          ${className}
        `}
        {...fieldProps}
        {...props}
      />
      
      {error && (
        <p 
          id={errorId}
          className="text-sm text-[var(--status-error)]"
          {...getStatusAriaProps('error')}
        >
          {error}
        </p>
      )}
    </div>
  );
});

AccessibleInput.displayName = 'AccessibleInput';

// ============ NOTIFICATION ACCESSIBLE ============

interface AccessibleNotificationProps {
  level: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  message: string;
  onClose?: () => void;
  autoClose?: boolean;
  duration?: number;
}

export const AccessibleNotification: React.FC<AccessibleNotificationProps> = ({
  level,
  title,
  message,
  onClose,
  autoClose = true,
  duration = 5000
}) => {
  const [isVisible, setIsVisible] = useState(true);
  const notificationRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (autoClose && level !== 'error') {
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => onClose?.(), 300);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [autoClose, duration, level, onClose]);

  useEffect(() => {
    // Focus sur la notification si c'est une erreur critique
    if (level === 'error' && notificationRef.current) {
      notificationRef.current.focus();
    }
  }, [level]);

  const levelConfig = {
    info: {
      bgColor: 'bg-[var(--status-info-bg)]',
      borderColor: 'border-[var(--status-info-border)]',
      textColor: 'text-[var(--status-info)]',
      icon: 'ℹ️'
    },
    success: {
      bgColor: 'bg-[var(--status-success-bg)]',
      borderColor: 'border-[var(--status-success-border)]',
      textColor: 'text-[var(--status-success)]',
      icon: '✅'
    },
    warning: {
      bgColor: 'bg-[var(--status-warning-bg)]',
      borderColor: 'border-[var(--status-warning-border)]',
      textColor: 'text-[var(--status-warning)]',
      icon: '⚠️'
    },
    error: {
      bgColor: 'bg-[var(--status-error-bg)]',
      borderColor: 'border-[var(--status-error-border)]',
      textColor: 'text-[var(--status-error)]',
      icon: '❌'
    }
  };

  const config = levelConfig[level];
  const statusProps = getStatusAriaProps(level);

  if (!isVisible) return null;

  return (
    <div
      ref={notificationRef}
      className={`
        ${config.bgColor} ${config.borderColor} ${config.textColor}
        border-l-4 p-4 rounded-r-lg shadow-lg
        transform transition-all duration-300 ease-in-out
        ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
        focus:outline-none focus:ring-2 focus:ring-[var(--accent-primary)]
      `}
      tabIndex={level === 'error' ? 0 : -1}
      {...statusProps}
    >
      <div className="flex items-start">
        <span className="text-lg mr-3" aria-hidden="true">{config.icon}</span>
        
        <div className="flex-1 min-w-0">
          {title && (
            <h4 className="font-semibold mb-1">
              {title}
            </h4>
          )}
          <p className="text-sm">
            {message}
          </p>
        </div>
        
        {onClose && (
          <AccessibleButton
            variant="secondary"
            size="sm"
            onClick={() => {
              setIsVisible(false);
              setTimeout(() => onClose(), 300);
            }}
            className="ml-3 p-1 min-h-[32px] min-w-[32px] hover:bg-black/10"
            aria-label="Fermer la notification"
          >
            <span aria-hidden="true">×</span>
          </AccessibleButton>
        )}
      </div>
    </div>
  );
};

// ============ MODAL ACCESSIBLE ============

interface AccessibleModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const AccessibleModal: React.FC<AccessibleModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md'
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const titleId = generateAriaId('modal-title');
  
  useFocusTrap(isOpen, modalRef);
  
  useEffect(() => {
    if (isOpen) {
      // Empêcher le scroll du body
      document.body.style.overflow = 'hidden';
      // Annoncer l'ouverture de la modal
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'assertive');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.textContent = `Modal ${title} ouverte`;
      document.body.appendChild(announcement);
      
      setTimeout(() => {
        document.body.removeChild(announcement);
      }, 1000);
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen, title]);

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 overflow-y-auto"
      aria-labelledby={titleId}
      role="dialog"
      aria-modal="true"
    >
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />
      
      {/* Modal Container */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div
          ref={modalRef}
          className={`
            relative w-full ${sizeClasses[size]}
            bg-[var(--bg-primary)] rounded-lg shadow-xl
            transform transition-all duration-200
            border border-[var(--border-primary)]
          `}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[var(--border-primary)]">
            <h2 
              id={titleId}
              className="text-lg font-semibold text-[var(--text-primary)]"
            >
              {title}
            </h2>
            <AccessibleButton
              variant="secondary"
              size="sm"
              onClick={onClose}
              className="p-2 min-h-[40px] min-w-[40px]"
              aria-label="Fermer la modal"
              data-close
            >
              <span aria-hidden="true">×</span>
            </AccessibleButton>
          </div>
          
          {/* Content */}
          <div className="p-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

// ============ GRAPHIQUE ACCESSIBLE ============

interface AccessibleChartProps {
  title: string;
  description: string;
  data: any[];
  children: React.ReactNode;
  className?: string;
}

export const AccessibleChart: React.FC<AccessibleChartProps> = ({
  title,
  description,
  data,
  children,
  className = ''
}) => {
  const chartId = generateAriaId('chart');
  const descId = generateAriaId('chart-desc');
  
  // Générer un résumé textuel des données
  const summary = `Graphique contenant ${data.length} points de données. ${description}`;
  
  return (
    <div className={`relative ${className}`}>
      <div className="sr-only">
        <h3 id={chartId}>{title}</h3>
        <p id={descId}>{summary}</p>
        
        {/* Table de données alternative pour lecteurs d'écran */}
        <table>
          <caption>Données du graphique {title}</caption>
          <thead>
            <tr>
              {Object.keys(data[0] || {}).map(key => (
                <th key={key} scope="col">{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 10).map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, cellIndex) => (
                  <td key={cellIndex}>{String(value)}</td>
                ))}
              </tr>
            ))}
            {data.length > 10 && (
              <tr>
                <td colSpan={Object.keys(data[0] || {}).length}>
                  ... et {data.length - 10} lignes supplémentaires
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Graphique visuel */}
      <div
        role="img"
        aria-labelledby={chartId}
        aria-describedby={descId}
        tabIndex={0}
        className="focus:outline-none focus:ring-2 focus:ring-[var(--accent-primary)] rounded"
      >
        {children}
      </div>
    </div>
  );
};

// ============ STYLES GLOBAUX POUR ACCESSIBILITÉ ============

export const AccessibilityStyles = `
  /* Focus visible pour navigation clavier */
  .keyboard-user *:focus {
    outline: 2px solid var(--accent-primary) !important;
    outline-offset: 2px;
  }

  /* Screen reader only */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* Skip link */
  .skip-link:focus {
    position: absolute !important;
    top: 6px !important;
    left: 6px !important;
    z-index: 1100;
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    :root {
      --border-primary: #000000;
      --text-primary: #000000;
      --bg-primary: #ffffff;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }

  /* Touch improvements */
  @media (hover: none) and (pointer: coarse) {
    button, [role="button"] {
      min-height: 48px;
      min-width: 48px;
    }
  }
`;

export default {
  AccessibleButton,
  AccessibleInput,
  AccessibleNotification,
  AccessibleModal,
  AccessibleChart,
  AccessibilityStyles
};
