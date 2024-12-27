class AuctionComponent extends owl.Component {
    static template = owl.xml`
      <div>
        <h3 class="auction-title">Auction: <t t-esc="state.auctionTitle" /></h3>
        <p>Current Highest Bid: ₹<t t-esc="state.highestBid" /></p>
      </div>
    `;
  
    setup() {
      this.state = owl.useState({
        highestBid: this.props.highestBid || 0,
        auctionTitle: this.props.auctionTitle || 'No Title'
      });
  
      this.auctionId = this.props.auctionId;
      this.busService = this.env.services.bus_service;
      this.channel = `auction_${this.auctionId}`;
  
      // Subscribe to the bus channel for auction updates
      this.busService.addChannel(this.channel);
      this.busService.addEventListener('auction_update', this.onBidUpdate.bind(this));
      console.log("hi")
    }

  
    // Handle incoming bid update
    onBidUpdate({ detail: notifications }) {
      notifications = notifications.filter(
        item => item.payload.auction_id === this.auctionId
      );
  
      notifications.forEach(item => {
        console.log("Received auction update:", item.payload);  // Debug log for received updates
        this.state.highestBid = item.payload.highest_bid;
      });
    }
  }
  