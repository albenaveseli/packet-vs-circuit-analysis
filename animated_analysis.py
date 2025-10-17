import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from scipy.stats import binom
import random
from collections import deque

class RealisticPacket:
    def __init__(self, user_id, packet_id, creation_time):
        self.user_id = user_id
        self.packet_id = packet_id
        self.creation_time = creation_time
        self.color = plt.cm.Set3(user_id % 12)
        self.size = random.randint(500, 1500)  # bytes
        self.position = [0, 0]
        self.status = "created"
        self.transmission_progress = 0
        self.bits_transmitted = 0
        self.start_transmission_time = None
        
    def update_transmission(self, available_bandwidth, dt):
        """Update packet transmission progress based on available bandwidth"""
        if self.start_transmission_time is None:
            self.start_transmission_time = self.creation_time
            
        bits_this_frame = available_bandwidth * dt
        bits_needed = self.size * 8 - self.bits_transmitted
        
        if bits_this_frame >= bits_needed:
            self.bits_transmitted = self.size * 8
            self.transmission_progress = 1.0
            return True
        else:
            self.bits_transmitted += bits_this_frame
            self.transmission_progress = self.bits_transmitted / (self.size * 8)
            return False

class RealisticPacketSwitch:
    def __init__(self, N_users, user_active_prob=0.1):
        self.N_users = N_users
        self.user_active_prob = user_active_prob
        self.link_capacity = 1e9  # 1 Gb/s
        self.user_capacity = 100e6  # 100 Mb/s
        
        # Network state
        self.users = [{'active': False, 'packets_sent': 0, 'position': [0, 0], 'id': i} for i in range(N_users)]
        self.packets = []
        self.buffer = deque()
        self.max_buffer_size = 50
        self.processed_packets = 0
        self.dropped_packets = 0
        self.time = 0
        self.dt = 0.05
        
        # Statistics
        self.active_users_history = []
        self.throughput_history = []
        self.loss_rate_history = []
        self.buffer_occupancy_history = []
        self.utilization_history = []
        self.time_history = []
        
        self.bytes_processed_this_second = 0
        self.last_throughput_update = 0
        self.current_throughput = 0
        self.current_utilization = 0
        self.current_loss_rate = 0
        self.current_active_users = 0
        
        self.theoretical_stats = self.calculate_theoretical_probabilities()
        
        self.setup_visualization()
    
    def calculate_theoretical_probabilities(self):
        n = self.N_users
        p = self.user_active_prob
        prob_more_than_10 = 1 - binom.cdf(10, n, p)
        expected_active = n * p
        max_supported_users = self.link_capacity / self.user_capacity
        prob_overload = 1 - binom.cdf(max_supported_users, n, p)
        return {
            'n': n,
            'p': p,
            'prob_more_than_10': prob_more_than_10,
            'expected_active': expected_active,
            'max_supported_users': max_supported_users,
            'prob_overload': prob_overload
        }
    
    def setup_visualization(self):
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.weight'] = 'bold'
        
        self.fig = plt.figure(figsize=(16, 10))
        
        # Create a 2x2 grid
        self.ax_physical = plt.subplot2grid((2, 2), (0, 0), colspan=2)
        self.ax_probability = plt.subplot2grid((2, 2), (1, 0))
        self.ax_buffer = plt.subplot2grid((2, 2), (1, 1))
        
        # Main title aligned to the left
        title_text = (f'📡 PACKET SWITCHING SIMULATION | 👥 {self.N_users} Users | '
                     f'🎯 P(X>10) = {self.theoretical_stats["prob_more_than_10"]:.6f} | '
                     f'⚡ 1 Gb/s Link | 📱 100 Mb/s per User')
        
        self.fig.suptitle(title_text, fontsize=13, fontweight='bold', y=0.98, x=0.02, ha='left')
        
        self.setup_physical_view()
        self.setup_probability_view()
        self.setup_buffer_view()
    
    def setup_physical_view(self):
        self.ax_physical.set_xlim(-2, 12)
        self.ax_physical.set_ylim(-1, 8)
        self.ax_physical.set_aspect('equal')
        self.ax_physical.set_title('🌐 NETWORK TOPOLOGY - Live Packet Flow', fontweight='bold', pad=10)
        self.ax_physical.grid(True, alpha=0.2)
        
        # Draw users in a circle
        radius = 5
        for i in range(self.N_users):
            angle = 2 * np.pi * i / self.N_users
            x = 1 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            self.users[i]['position'] = [x, y]
            
            user_circle = Circle((x, y), 0.25, color='lightblue', alpha=0.8, ec='darkblue', linewidth=1)
            self.ax_physical.add_patch(user_circle)
            self.ax_physical.text(x, y, str(i), ha='center', va='center', 
                                fontsize=7, weight='bold', color='darkblue')
        
        # Draw switch with better styling
        switch_rect = Rectangle((5.5, 3), 1, 2, color='red', alpha=0.8, ec='darkred', linewidth=2)
        self.ax_physical.add_patch(switch_rect)
        self.ax_physical.text(6, 4, 'SWITCH\n1 Gb/s', ha='center', va='center', 
                            fontsize=9, weight='bold', color='white')
        
        # Draw buffer area
        buffer_bg = Rectangle((7, 3), 0.4, 2, color='lightgray', alpha=0.5, ec='gray')
        self.ax_physical.add_patch(buffer_bg)
        self.buffer_fill = Rectangle((7, 3), 0.4, 0, color='orange', alpha=0.8, ec='darkorange')
        self.ax_physical.add_patch(self.buffer_fill)
        
        # Draw destination
        dest_rect = Rectangle((8, 3.5), 1.2, 1, color='green', alpha=0.8, ec='darkgreen', linewidth=2)
        self.ax_physical.add_patch(dest_rect)
        self.ax_physical.text(8.6, 4, 'INTERNET', ha='center', va='center', 
                            fontsize=9, weight='bold', color='white')
        
        # Add connection lines
        self.ax_physical.plot([1.25, 5.5], [4, 4], 'k--', alpha=0.3, linewidth=1)
        self.ax_physical.plot([6.5, 7], [4, 4], 'k--', alpha=0.3, linewidth=1)
        self.ax_physical.plot([7.4, 8], [4, 4], 'k--', alpha=0.3, linewidth=1)
        
        # Add real-time statistics text - moved to left side
        self.stats_text = self.ax_physical.text(0.02, 0.98, '', transform=self.ax_physical.transAxes,
                                              fontsize=9, weight='bold', verticalalignment='top',
                                              bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))
    
    def setup_probability_view(self):
        self.ax_probability.set_title('📊 PROBABILITY DISTRIBUTION', fontweight='bold', pad=10)
        self.ax_probability.set_xlabel('Number of Active Users')
        self.ax_probability.set_ylabel('Probability')
        self.ax_probability.grid(True, alpha=0.2)
        
        n = self.N_users
        p = self.user_active_prob
        x = np.arange(0, min(n + 1, 25))
        pmf = binom.pmf(x, n, p)
        
        self.prob_bars = self.ax_probability.bar(x, pmf, alpha=0.8, color='skyblue', 
                                               edgecolor='navy', linewidth=1)
        
        # Mark critical regions
        max_supported = self.theoretical_stats['max_supported_users']
        self.ax_probability.axvline(x=max_supported, color='red', linestyle='-', 
                                  linewidth=3, alpha=0.7, label=f'Capacity Limit ({max_supported} users)')
        self.ax_probability.axvline(x=10, color='orange', linestyle='--', 
                                  linewidth=2, alpha=0.7, label='X=10 threshold')
        
        # Color bars based on overload probability
        for i, bar in enumerate(self.prob_bars):
            if i > max_supported:
                bar.set_color('red')
                bar.set_alpha(0.9)
            elif i > 10:
                bar.set_color('orange')
                bar.set_alpha(0.9)
        
        self.ax_probability.legend(fontsize=8)
        
        # Add probability text with better formatting
        prob_text = (f'🎲 Probability Analysis:\n'
                    f'P(X > 10) = {self.theoretical_stats["prob_more_than_10"]:.6f}\n'
                    f'P(Overload) = {self.theoretical_stats["prob_overload"]:.6f}\n'
                    f'E[X] = {self.theoretical_stats["expected_active"]:.2f} users\n'
                    f'Max Capacity: {max_supported:.0f} users')
        
        self.ax_probability.text(0.65, 0.95, prob_text, transform=self.ax_probability.transAxes,
                               fontsize=8, bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8),
                               verticalalignment='top')
    
    def setup_buffer_view(self):
        self.ax_buffer.set_title('💾 BUFFER & SYSTEM STATUS', fontweight='bold', pad=10)
        self.ax_buffer.set_xlim(-1, 2)
        self.ax_buffer.set_ylim(-1, 1)
        self.ax_buffer.set_aspect('equal')
        self.ax_buffer.axis('off')
        
        # Buffer visualization with better styling
        buffer_outline = FancyBboxPatch((0, -0.8), 0.3, 1.6, boxstyle="round,pad=0.05", 
                                      facecolor="lightgray", alpha=0.6, ec="gray", linewidth=2)
        self.ax_buffer.add_patch(buffer_outline)
        
        # Buffer title
        self.ax_buffer.text(0.15, 0.9, 'BUFFER', ha='center', va='center', 
                          fontsize=11, weight='bold', color='darkblue')
        
        # Performance metrics box
        self.metrics_text = self.ax_buffer.text(0.15, -0.2, '', ha='center', va='top', 
                                              fontsize=9, weight='bold',
                                              bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    def update_users(self):
        active_count = 0
        for user in self.users:
            if random.random() < self.user_active_prob:
                user['active'] = True
                active_count += 1
                # Generate packets with higher probability during activity
                if random.random() < 0.7:  # Increased to see more action
                    packet = RealisticPacket(user['id'], len(self.packets), self.time)
                    packet.position = user['position'].copy()
                    packet.status = "transmitting"
                    self.packets.append(packet)
                    user['packets_sent'] += 1
            else:
                user['active'] = False
        return active_count
    
    def update_packets(self, active_count):
        # Calculate available bandwidth
        if active_count > 0:
            total_demand = active_count * self.user_capacity
            if total_demand > self.link_capacity:
                available_bandwidth_per_user = self.link_capacity / active_count
            else:
                available_bandwidth_per_user = self.user_capacity
        else:
            available_bandwidth_per_user = 0
        
        packets_to_remove = []
        current_throughput_bytes = 0
        
        for packet in self.packets:
            if packet.status == "transmitting":
                transmission_complete = packet.update_transmission(available_bandwidth_per_user, self.dt)
                
                if transmission_complete:
                    if len(self.buffer) < self.max_buffer_size:
                        packet.status = "buffered"
                        self.buffer.append(packet)
                    else:
                        packet.status = "dropped"
                        packets_to_remove.append(packet)
                        self.dropped_packets += 1
            
            elif packet.status == "buffered":
                # Update position in buffer visualization
                try:
                    index = list(self.buffer).index(packet)
                    packet.position = [7.2, 3 + (index * 0.07)]
                except ValueError:
                    pass
            
            elif packet.status == "processing":
                # Move packet toward destination
                packet.position[0] += 3.0 * self.dt
                if packet.position[0] > 9.0:
                    packet.status = "delivered"
                    packets_to_remove.append(packet)
                    self.processed_packets += 1
                    current_throughput_bytes += packet.size
        
        # Update throughput
        self.bytes_processed_this_second += current_throughput_bytes
        
        # Remove processed packets
        for packet in packets_to_remove:
            if packet in self.packets:
                self.packets.remove(packet)
        
        # Process packets from buffer
        processing_capacity = 8  # packets per time step
        packets_processed = 0
        
        while self.buffer and packets_processed < processing_capacity:
            packet = self.buffer.popleft()
            packet.status = "processing"
            packet.position = [7.6, 4]  # Start processing position
            packets_processed += 1
    
    def update_statistics(self, active_count):
        self.current_active_users = active_count
        
        # Update throughput and utilization every second
        if self.time - self.last_throughput_update >= 1.0:
            throughput_mbps = (self.bytes_processed_this_second * 8) / 1e6
            self.current_throughput = throughput_mbps
            
            # Calculate utilization
            self.current_utilization = min(100, (throughput_mbps / 1000) * 100)
            
            self.bytes_processed_this_second = 0
            self.last_throughput_update = self.time
        
        # Calculate loss rate
        total_packets = self.processed_packets + self.dropped_packets
        self.current_loss_rate = (self.dropped_packets / total_packets * 100) if total_packets > 0 else 0
        
        # Buffer occupancy
        self.current_buffer_occupancy = (len(self.buffer) / self.max_buffer_size) * 100
    
    def update_visualization(self, active_count):
        self.update_physical_view(active_count)
        self.update_buffer_view()
    
    def update_physical_view(self, active_count):
        # Clear only dynamic elements (users and packets)
        for patch in self.ax_physical.patches[:]:
            if isinstance(patch, Circle):
                patch.remove()
        
        # Update users with activity status
        for user in self.users:
            color = 'limegreen' if user['active'] else 'lightblue'
            user_circle = Circle(user['position'], 0.25, color=color, alpha=0.9, 
                               ec='darkgreen' if user['active'] else 'darkblue', linewidth=2)
            self.ax_physical.add_patch(user_circle)
            
            # User ID text
            self.ax_physical.text(user['position'][0], user['position'][1], str(user['id']), 
                                ha='center', va='center', fontsize=7, weight='bold', 
                                color='white' if user['active'] else 'darkblue')
        
        # Update buffer fill with smooth color transition
        buffer_fill_height = (len(self.buffer) / self.max_buffer_size) * 2
        self.buffer_fill.set_height(buffer_fill_height)
        
        fill_ratio = len(self.buffer) / self.max_buffer_size
        if fill_ratio > 0.8:
            self.buffer_fill.set_color('red')
        elif fill_ratio > 0.5:
            self.buffer_fill.set_color('orange')
        else:
            self.buffer_fill.set_color('limegreen')
        
        # Draw packets with better visualization
        for packet in self.packets:
            if packet.status == "transmitting":
                # Animate packet movement from user to switch
                start_pos = self.users[packet.user_id]['position']
                end_pos = [6, 4]
                
                progress = packet.transmission_progress
                packet.position[0] = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
                packet.position[1] = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
                
                # Larger, more visible packets
                packet_circle = Circle(packet.position, 0.12, color=packet.color, alpha=0.9,
                                     ec='black', linewidth=1)
                self.ax_physical.add_patch(packet_circle)
            
            elif packet.status in ["buffered", "processing"]:
                packet_circle = Circle(packet.position, 0.1, color=packet.color, alpha=0.9,
                                     ec='black', linewidth=1)
                self.ax_physical.add_patch(packet_circle)
        
        # Update real-time statistics
        stats_text = (f'📊 REAL-TIME STATISTICS:\n'
                     f'⏱️  Time: {self.time:.1f}s\n'
                     f'👥 Active Users: {self.current_active_users}/{self.N_users}\n'
                     f'⚡ Utilization: {self.current_utilization:.1f}%\n'
                     f'📦 Throughput: {self.current_throughput:.1f} Mb/s\n'
                     f'❌ Loss Rate: {self.current_loss_rate:.1f}%\n'
                     f'💾 Buffer: {len(self.buffer)}/{self.max_buffer_size} ({self.current_buffer_occupancy:.1f}%)\n'
                     f'📨 Processed: {self.processed_packets} | ❌ Dropped: {self.dropped_packets}')
        
        self.stats_text.set_text(stats_text)
    
    def update_buffer_view(self):
        # Clear previous buffer packets
        for patch in self.ax_buffer.patches[1:]:  # Keep the outline
            patch.remove()
        
        # Draw packets in buffer with better visualization
        for i, packet in enumerate(list(self.buffer)[:18]):  # Show more packets
            y_pos = 0.5 - (i * 0.08)
            packet_rect = Rectangle((0.03, y_pos), 0.24, 0.06, 
                                  color=packet.color, alpha=0.9,
                                  ec='black', linewidth=0.5)
            self.ax_buffer.add_patch(packet_rect)
        
        # Update performance metrics
        transmitting_count = sum(1 for p in self.packets if p.status == "transmitting")
        processing_count = sum(1 for p in self.packets if p.status == "processing")
        
        metrics_text = (f'🚀 PERFORMANCE METRICS:\n'
                       f'📦 Packets in System: {len(self.packets)}\n'
                       f'  ├ Transmitting: {transmitting_count}\n'
                       f'  ├ In Buffer: {len(self.buffer)}\n'
                       f'  └ Processing: {processing_count}\n'
                       f'⚡ System Status:\n')
        
        if self.current_utilization > 90:
            metrics_text += '  🔴 CRITICAL - High Load'
        elif self.current_utilization > 70:
            metrics_text += '  🟠 WARNING - Medium Load'
        else:
            metrics_text += '  🟢 NORMAL - Low Load'
            
        if self.current_loss_rate > 5:
            metrics_text += '\n  ❌ HIGH PACKET LOSS'
        
        self.metrics_text.set_text(metrics_text)
    
    def update(self, frame):
        self.time += self.dt
        active_count = self.update_users()
        self.update_packets(active_count)
        self.update_statistics(active_count)
        self.update_visualization(active_count)
        return []

def run_comparison_simulations():
    """Run simulations for different user counts"""
    scenarios = [
        (10, 0.1, "N=10 (Optimal)"),
        (35, 0.1, "N=35 (Good)"), 
        (50, 0.1, "N=50 (High Load)"),
        (100, 0.1, "N=100 (Overload)")
    ]
    
    for N, p, description in scenarios:
        print(f"\n{'='*70}")
        print(f"🚀 SIMULATING: {description}")
        print(f"{'='*70}")
        
        # Calculate theoretical probabilities
        prob_more_than_10 = 1 - binom.cdf(10, N, p)
        max_supported_users = 10
        prob_overload = 1 - binom.cdf(max_supported_users, N, p)
        
        print(f"📊 Theoretical Analysis:")
        print(f"   P(X > 10) = {prob_more_than_10:.6f}")
        print(f"   P(Overload) = {prob_overload:.6f}")
        print(f"   Expected active users: {N * p:.1f}")
        print(f"   Max supported users: {max_supported_users}")
        
        # Create and run simulation
        sim = RealisticPacketSwitch(N, p)
        
        # Create animation
        anim = animation.FuncAnimation(
            sim.fig, sim.update, frames=500, interval=40, blit=False, repeat=True
        )
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92, hspace=0.3, wspace=0.3)
        plt.show()

if __name__ == "__main__":
    print("🎯 REALISTIC PACKET SWITCHING SIMULATION")
    print("=" * 70)
    
    # Show probability comparison table
    print("\n📋 PROBABILITY COMPARISON:")
    print("┌─────────┬───────────────┬─────────────────┬──────────────┐")
    print("│ N Users │   P(X > 10)   │ Expected Active │    Status    │")
    print("├─────────┼───────────────┼─────────────────┼──────────────┤")
    
    for N in [10, 35, 50, 100]:
        p = 0.1
        prob_more_than_10 = 1 - binom.cdf(10, N, p)
        expected_active = N * p
        status = "🔴 OVERLOAD" if expected_active > 10 else "🟢 SAFE"
        
        print(f"│ {N:7} │ {prob_more_than_10:13.6f} │ {expected_active:15.1f} │ {status:12} │")
    
    print("└─────────┴───────────────┴─────────────────┴──────────────┘")
    
    print("\n📍 Key Insights:")
    print("   • P(X>10) shows probability of exceeding capacity")
    print("   • System overloads when expected users > 10")
    print("   • Packet loss occurs during overload conditions")
    print("   • Watch the buffer fill up during high load!")
    
    input("\n🎬 Press Enter to start animations...")
    run_comparison_simulations()