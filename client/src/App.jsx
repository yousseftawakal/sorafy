import { ReactComponent as LogoH } from './assets/Sorafy - horizontal.svg';
import './styles/main.scss';
import { useState } from 'react';
import React from 'react';
import {
  MdImage,
  MdAutoFixHigh,
  MdSettings,
  MdAdd,
  MdDownload,
  MdChangeCircle,
  MdClearAll,
  MdCheck,
} from 'react-icons/md';
import { PiWaveform } from 'react-icons/pi';

function App() {
  const [activeTab, setActiveTab] = useState('all');
  const [activeProcessors, setActiveProcessors] = useState([]);
  const [sourceImage, setSourceImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [availableEffects, setAvailableEffects] = useState({});
  const [error, setError] = useState(null);
  const [processorParams, setProcessorParams] = useState({});
  const [pendingChanges, setPendingChanges] = useState({});
  const fileInputRef = React.useRef(null);

  const API_URL = 'http://127.0.0.1:5000';

  React.useEffect(() => {
    const fetchEffects = async () => {
      try {
        const response = await fetch(`${API_URL}/effects`);
        if (!response.ok) {
          throw new Error('Failed to fetch effects');
        }
        const data = await response.json();
        setAvailableEffects(data);
      } catch (error) {
        setError('Failed to load effects. Please refresh the page.');
      }
    };
    fetchEffects();
  }, []);

  const handleParamChange = (processorId, paramId, value) => {
    const newValue = parseFloat(value);

    setPendingChanges((prev) => ({
      ...prev,
      [processorId]: {
        ...prev[processorId],
        [paramId]: newValue,
      },
    }));
  };

  const applyProcessorChanges = (processorId) => {
    if (!pendingChanges[processorId]) return;

    const currentPendingChanges = pendingChanges[processorId];

    const tempParams = {
      ...processorParams,
      [processorId]: {
        ...processorParams[processorId],
        ...currentPendingChanges,
      },
    };

    applyProcessors(tempParams);

    setProcessorParams(tempParams);

    setPendingChanges((prev) => {
      const newPending = { ...prev };
      delete newPending[processorId];
      return newPending;
    });
  };

  const applyAllChanges = () => {
    const currentPendingChanges = { ...pendingChanges };

    const tempParams = { ...processorParams };
    Object.entries(currentPendingChanges).forEach(([processorId, params]) => {
      tempParams[processorId] = {
        ...tempParams[processorId],
        ...params,
      };
    });

    applyProcessors(tempParams);

    setProcessorParams(tempParams);

    setPendingChanges({});
  };

  const toggleProcessor = (processorId) => {
    setActiveProcessors((prev) => {
      const isAdding = !prev.includes(processorId);
      const newProcessors = isAdding
        ? [...prev, processorId]
        : prev.filter((id) => id !== processorId);

      if (isAdding) {
        const effect = availableEffects[processorId];
        if (effect && effect.params) {
          const defaultParams = {};
          effect.params.forEach((param) => {
            defaultParams[param.id] = param.default;
          });

          setProcessorParams((prev) => ({
            ...prev,
            [processorId]: defaultParams,
          }));
        }
      } else {
        setProcessorParams((prev) => {
          const newParams = { ...prev };
          delete newParams[processorId];
          return newParams;
        });
      }

      return newProcessors;
    });
  };

  const handleImageUpload = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSourceImage(e.target.result);
        setProcessedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleImageUpload(file);
    }
  };

  const applyProcessors = async (overrideParams = null) => {
    if (!sourceImage || activeProcessors.length === 0) return;

    setIsProcessing(true);
    setError(null);
    try {
      const base64Data = sourceImage.split(',')[1];

      const blob = await fetch(`data:image/png;base64,${base64Data}`).then(
        (res) => res.blob()
      );

      const formData = new FormData();
      formData.append('image', blob, 'image.png');

      const effects = activeProcessors.map((id) => {
        const params = overrideParams?.[id] || processorParams[id] || {};
        return {
          id,
          params,
        };
      });
      formData.append('effects', JSON.stringify(effects));

      const response = await fetch(`${API_URL}/process`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        try {
          const errorData = JSON.parse(errorText);
          throw new Error(
            `Failed to process image: ${errorData.error || response.statusText}`
          );
        } catch (e) {
          throw new Error(
            `Failed to process image: ${errorText || response.statusText}`
          );
        }
      }

      const data = await response.json();
      setProcessedImage(`data:image/png;base64,${data.image}`);
    } catch (error) {
      setError(`Failed to process image: ${error.message}`);
      setProcessedImage(sourceImage);
    } finally {
      setIsProcessing(false);
    }
  };

  React.useEffect(() => {
    if (sourceImage && activeProcessors.length > 0) {
      applyProcessors();
    } else if (activeProcessors.length === 0) {
      setProcessedImage(sourceImage);
    }
  }, [activeProcessors]);

  const handleDownload = () => {
    if (!processedImage) return;

    const link = document.createElement('a');
    link.href = processedImage;
    link.download = `output_${Date.now()}`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="App">
      <Header />
      <main className="main">
        {error && <div className="error-message">{error}</div>}
        <section className="container">
          <Card
            icon={<MdImage size={20} />}
            heading="Source Signal"
            paragraph="Upload an image to process"
            btn={
              sourceImage
                ? {
                    text: 'Change',
                    icon: <MdChangeCircle size={16} />,
                    onClick: () => fileInputRef.current?.click(),
                  }
                : null
            }
          >
            <input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              style={{ display: 'none' }}
              onChange={handleFileInput}
            />
            {!sourceImage ? (
              <Upload
                onUpload={handleImageUpload}
                fileInputRef={fileInputRef}
              />
            ) : (
              <Canvas label="source.img" image={sourceImage} />
            )}
          </Card>

          <Card
            icon={<MdAutoFixHigh size={20} />}
            heading="Processed Output"
            paragraph={`Applied effects: ${activeProcessors.length}`}
            btn={{
              text: 'Download',
              icon: <MdDownload size={16} />,
              onClick: handleDownload,
              disabled: !processedImage || isProcessing,
            }}
          >
            <Canvas
              label="processed.img"
              image={processedImage}
              isProcessing={isProcessing}
            />
          </Card>
        </section>

        <Card
          icon={<MdSettings size={20} />}
          heading="Signal Processors"
          paragraph="Select effects and adjust parameters to process your image"
          className="processors-card"
        >
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'all' ? 'active' : ''}`}
              onClick={() => setActiveTab('all')}
            >
              ALL PROCESSORS
            </button>
            <button
              className={`tab ${activeTab === 'active' ? 'active' : ''}`}
              onClick={() => setActiveTab('active')}
            >
              ACTIVE ({activeProcessors.length})
            </button>
          </div>

          <div className="processors">
            {Object.entries(availableEffects)
              .filter(
                ([id, _]) =>
                  activeTab === 'all' || activeProcessors.includes(id)
              )
              .map(([id, effect]) => (
                <Processor
                  key={id}
                  name={effect.name}
                  description={effect.description}
                  active={activeProcessors.includes(id)}
                  onToggle={() => toggleProcessor(id)}
                  hasPendingChanges={!!pendingChanges[id]}
                  onApply={() => applyProcessorChanges(id)}
                >
                  {effect.params.map((param) => (
                    <Slider
                      key={param.id}
                      label={param.name}
                      min={param.min}
                      max={param.max}
                      step={param.step}
                      defaultValue={param.default}
                      value={
                        pendingChanges[id]?.[param.id] ??
                        processorParams[id]?.[param.id] ??
                        param.default
                      }
                      onChange={(value) =>
                        handleParamChange(id, param.id, value)
                      }
                    />
                  ))}
                </Processor>
              ))}
          </div>

          <div className="processors-footer">
            <Button
              type={2}
              text="CLEAR ALL"
              icon={<MdClearAll size={16} />}
              onClick={() => {
                setActiveProcessors([]);
                setProcessorParams({});
                setPendingChanges({});
              }}
            />
            <Button
              type={1}
              text="APPLY ALL"
              icon={<MdCheck size={16} />}
              onClick={applyAllChanges}
              disabled={Object.keys(pendingChanges).length === 0}
            />
          </div>
        </Card>
      </main>
    </div>
  );
}

function Header() {
  return (
    <header className="header">
      <LogoH className="logo" />
    </header>
  );
}

function Card({ heading, paragraph, btn, children, icon }) {
  return (
    <div className="card">
      <div className="card__header">
        <div className="card__header__container">
          <div className="icon--sm">{icon}</div>
          <div className="card__header_typo">
            <h1 className="heading">
              {heading}
              <span className="dot"></span>
            </h1>
            <p className="paragraph--2">{paragraph}</p>
          </div>
        </div>
        {btn && (
          <Button
            className="card__btn"
            type={2}
            icon={btn.icon}
            text={btn.text}
            onClick={btn.onClick}
          />
        )}
      </div>
      <div className="card__body">{children}</div>
    </div>
  );
}

function Upload({ onUpload, fileInputRef }) {
  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      onUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUploadClick = (e) => {
    e.stopPropagation();
    fileInputRef.current?.click();
  };

  return (
    <div
      className="upload"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onClick={handleUploadClick}
    >
      <div className="icon--lg">
        <MdImage size={24} />
      </div>
      <p className="paragraph--3">// Drag and drop image or click to browse</p>
      <Button
        type={1}
        icon={<MdAdd size={16} />}
        text="Upload image"
        onClick={handleUploadClick}
      />
    </div>
  );
}

function Canvas({ label, image, isProcessing }) {
  const canvasRef = React.useRef(null);
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    if (image && canvasRef.current && containerRef.current) {
      const canvas = canvasRef.current;
      const container = containerRef.current;
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = () => {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;

        const containerRatio = canvas.width / canvas.height;
        const imageRatio = img.width / img.height;
        let drawWidth, drawHeight, x, y;

        if (containerRatio > imageRatio) {
          drawHeight = canvas.height;
          drawWidth = drawHeight * imageRatio;
          x = (canvas.width - drawWidth) / 2;
          y = 0;
        } else {
          drawWidth = canvas.width;
          drawHeight = drawWidth / imageRatio;
          x = 0;
          y = (canvas.height - drawHeight) / 2;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, x, y, drawWidth, drawHeight);
      };

      img.src = image;

      const handleResize = () => {
        if (img.complete) {
          img.onload();
        }
      };

      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [image]);

  return (
    <div
      className={`canvas__container ${isProcessing ? 'processing' : ''}`}
      ref={containerRef}
    >
      <div className="canvas__border"></div>
      <div className="canvas__border"></div>
      <div className="canvas__border"></div>
      <div className="canvas__border"></div>
      <canvas ref={canvasRef} className="canvas"></canvas>
      <div className="canvas__label">{label}</div>
      {isProcessing && (
        <div className="canvas__processing">
          <div className="canvas__processing__spinner"></div>
          <p>Processing...</p>
        </div>
      )}
    </div>
  );
}

function Button({
  type,
  icon,
  text,
  onClick,
  className,
  disabled,
  size = 'normal',
}) {
  const handleClick = (e) => {
    e.stopPropagation();
    onClick?.(e);
  };

  return (
    <button
      className={`btn btn--${type} ${className || ''} ${
        disabled ? 'disabled' : ''
      } ${size === 'small' ? 'btn--small' : ''}`}
      onClick={handleClick}
      disabled={disabled}
    >
      {icon && <div className={`btn--${type}__icon`}>{icon}</div>}
      {text}
    </button>
  );
}

function Processor({
  name,
  description,
  active,
  onToggle,
  children,
  hasPendingChanges,
  onApply,
}) {
  return (
    <div className={`processor ${active ? 'active' : ''}`}>
      <div
        className="processor__header"
        onClick={onToggle}
        style={{ cursor: 'pointer' }}
      >
        <div className="processor__info">
          <h3 className="processor__name">
            {name}
            <span className="processor__icon">
              <PiWaveform size={16} />
            </span>
          </h3>
          <p className="processor__description">{description}</p>
        </div>
        <div className="processor__status">
          {active ? 'ACTIVE' : 'INACTIVE'}
        </div>
      </div>
      {active && (
        <div className="processor__controls">
          {children}
          {hasPendingChanges && (
            <Button
              type={2}
              text="APPLY"
              icon={<MdCheck size={14} />}
              onClick={onApply}
              className="processor__apply-btn"
              size="small"
            />
          )}
        </div>
      )}
    </div>
  );
}

function Slider({ label, min, max, step, defaultValue, value, onChange }) {
  const handleChange = (e) => {
    const newValue = parseFloat(e.target.value);
    onChange?.(newValue);
  };

  return (
    <div className="slider">
      <div className="slider__header">
        <span className="slider__label">{label}</span>
        <span className="slider__value">{value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        className="slider__input"
      />
    </div>
  );
}

export default App;
