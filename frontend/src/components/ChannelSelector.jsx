import React from 'react';

const ChannelSelector = ({ language, channelId, setChannelId, channels }) => {
  return (
    <label className="flex items-center gap-2 min-w-0 max-w-full">
      <span className="sr-only">{language === 'hi' ? 'चैनल' : 'Channel'}</span>
      <select
        value={channelId}
        onChange={(event) => setChannelId(event.target.value)}
        className="touch-target bg-white/5 border border-white/20 text-white text-base rounded-xl px-2.5 max-w-[min(46vw,16rem)] truncate"
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
