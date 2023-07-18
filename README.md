# python-slot
An advanced, text-based Python slot machine

## Features
- True random generation via the [random.org API](https://www.random.org/clients/http/)
- Spinning animation always landing on the pre-generated winning row
- "Prop" rows in the animation that are not winnable are generated via Python pseudorandom library to cut down on API requests
- Balance system with configurable min and max bets

## Drawbacks
- Not usable without internet due to reliance on [random.org API](https://www.random.org/clients/http/) calls
- RTP not determined (I am not a mathematician!)

# Setup
1. Download and extract the source code
2. Ensure you have all the dependencies installed! (requests)
3. Sign up for a [random.org account](https://random.org) and generate a free [random.org API key](https://api.random.org/dashboard)
4. Set the value of the API_KEY constant to your newly generated API key
5. Run the program and have fun!
