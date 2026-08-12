import React from 'react';

const ChannelSelector = ({ language, channelId, setChannelId, channels }) => {
  return (
    <label className="flex items-center gap-2 min-w-0">
      <span className="sr-only">{language === 'hi' ? 'चैनल' : 'Channel'}</span>
      <select
        value={channelId}
        onChange={(event) => setChannelId(event.target.value)}
        className="bg-white/5 border border-white/20 text-white text-xs rounded-lg px-2 py-1 max-w-[46vw] truncate"
        aria-label={language === 'hi' ? 'चैनल चुनें' : 'Choose channel'}
      >
        {(channels || []).map((channel) => (
          <option key={channel.id} value={channel.id} className="text-black">
            {language === 'hi' ? (channel.name_hi || channel.name) : channel.name}
          </option>
        ))}
      </select>
    </label>
  );
};

export default ChannelSelector;
