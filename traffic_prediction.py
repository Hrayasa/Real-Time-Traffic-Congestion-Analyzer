import folium
import random
import numpy as np

class BangaloreTrafficAnalyzer:
    """
    A traffic congestion analysis tool specifically designed for Bangalore, India.
    
    Provides insights into traffic patterns using simulated data and interactive visualization.
    """
    
    def __init__(self, num_points=15):
        """
        Initialize the Bangalore Traffic Analyzer.
        
        :param num_points: Number of traffic data collection points
        """
        # Coordinates for Bangalore city center
        self.city_center = (12.9716, 77.5946)  # Latitude, Longitude for Bangalore
        self.num_points = num_points
        
        # List of major areas in Bangalore for more realistic data point distribution
        self.bangalore_areas = [
            "Indiranagar", "Koramangala", "Electronic City", 
            "Whitefield", "Marathahalli", "HSR Layout", 
            "Jayanagar", "JP Nagar", "BTM Layout", 
            "Rajajinagar"
        ]
    
    def generate_traffic_data(self):
        """
        Generate synthetic traffic congestion data for Bangalore.
        
        :return: List of congestion values between 0-100
        """
        try:
            # Simulate traffic congestion with higher variability
            # Most areas range between 40-80 to reflect Bangalore's typical traffic conditions
            return list(np.random.randint(40, 81, self.num_points))
        except Exception as e:
            print(f"Error generating traffic data: {e}")
            return [random.randint(40, 80) for _ in range(self.num_points)]
    
    def predict_congestion(self, data, window_size=3):
        """
        Predict future congestion using a moving average method.
        
        :param data: Historical traffic congestion data
        :param window_size: Number of recent data points to consider
        :return: Predicted congestion level
        """
        if not data:
            return 50  # Default congestion level for Bangalore
        
        window_size = min(window_size, len(data))
        return np.mean(data[-window_size:])
    
    def visualize_traffic(self, data, prediction):
        """
        Create an interactive map visualization of Bangalore traffic congestion.
        
        :param data: List of congestion data points
        :param prediction: Predicted congestion level
        """
        # Create map centered on Bangalore
        bangalore_map = folium.Map(
            location=self.city_center, 
            zoom_start=11,  # Slightly lower zoom to cover more of the city
            tiles='CartoDB positron'  # Clean, light map style
        )
        
        # Color mapping based on congestion levels
        def get_marker_color(congestion):
            if congestion < 50:
                return "green"  # Low congestion
            elif congestion < 70:
                return "orange"  # Medium congestion
            else:
                return "red"  # High congestion
        
        # Add data point markers for each area
        for i, congestion in enumerate(data):
            # Generate realistic location near Bangalore city center
            marker_location = (
                self.city_center[0] + random.uniform(-0.1, 0.1),
                self.city_center[1] + random.uniform(-0.1, 0.1)
            )
            
            folium.Marker(
                location=marker_location,
                popup=f"Area: {self.bangalore_areas[i % len(self.bangalore_areas)]}\nCongestion: {congestion}%",
                icon=folium.Icon(
                    color=get_marker_color(congestion), 
                    icon="car"  # Car icon to represent traffic
                )
            ).add_to(bangalore_map)
        
        # Add prediction marker
        prediction_location = (
            self.city_center[0] + random.uniform(-0.1, 0.1),
            self.city_center[1] + random.uniform(-0.1, 0.1)
        )
        
        folium.Marker(
            location=prediction_location,
            popup=f"Predicted City Congestion: {prediction:.2f}%",
            icon=folium.Icon(color="purple", icon="info-sign")
        ).add_to(bangalore_map)
        
        # Save the map
        map_filename = "bangalore_traffic_congestion_map.html"
        bangalore_map.save(map_filename)
        print(f"Bangalore traffic congestion map saved to {map_filename}")
    
    def run_analysis(self):
        """
        Orchestrate the entire traffic analysis workflow for Bangalore.
        """
        # Generate traffic data
        traffic_data = self.generate_traffic_data()
        
        # Predict congestion
        predicted_congestion = self.predict_congestion(traffic_data)
        
        # Visualize results
        self.visualize_traffic(traffic_data, predicted_congestion)

def main():
    """
    Main entry point for the Bangalore traffic analysis script.
    """
    try:
        # Create analyzer for Bangalore
        bangalore_traffic = BangaloreTrafficAnalyzer(num_points=10)
        
        # Run full analysis
        bangalore_traffic.run_analysis()
    
    except Exception as e:
        print(f"An error occurred during Bangalore traffic analysis: {e}")

if __name__ == "__main__":
    main()