from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta


"""
https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
"""
class GAExplorer:

    def __init__(self, file_path=None, view_id=None):
        self.filePath = file_path
        self.viewId = view_id

    def initialize_analyticsreporting(self):
        """Initializes an Analytics Reporting API V4 service object.

        Returns:
        An authorized Analytics Reporting API V4 service object.
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.filePath, ['https://www.googleapis.com/auth/analytics.readonly'])

        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials)

        return analytics

    def get_report(self, analytics, ga_date_ranges, ga_metics, ga_dimensions):
        """Queries the Analytics Reporting API V4.

        Args:
        analytics: An authorized Analytics Reporting API V4 service object.
        ga_date_ranges
        ga_metics
        ga_dimensions
        Returns:
        The Analytics Reporting API V4 response.
        """
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': self.viewId,
                        'dateRanges': ga_date_ranges,
                        'metrics': ga_metics,
                        'dimensions': ga_dimensions
                    }
                ]
            }).execute()

    def week_report_by_days(self):
        """Parses and reorganize Analytics Reporting API V4 response.

        Args:
        response: An Analytics Reporting API V4 response reorganized.
        """
        analytics = self.initialize_analyticsreporting()
        response = self.get_report(
            analytics,
            ga_date_ranges=[{'startDate': '8daysAgo', 'endDate': 'yesterday'}],
            ga_metics=[{'expression': 'ga:sessions'}],
            ga_dimensions=[
                {'name': 'ga:nthDay'},
                {'name': 'ga:source'}
            ]
        )

        # get all metrics name
        source_metrics = []
        for row in response.get('reports', [])[0].get('data', {}).get('rows', []):
            if row["dimensions"][1] not in source_metrics:
                source_metrics.append(row["dimensions"][1])

        dates_range = []
        for i in range(1, 8):
            dates_range.append(datetime.now() - timedelta(days=(8 - i)))

        final_dict = {}
        for d in dates_range:
            final_dict[d] = {}

        for x in final_dict:
            for y in source_metrics:
                final_dict[x][y] = 0

        for report in response.get('reports', []):
            column_header = report.get('columnHeader', {})
            dimension_headers = column_header.get('dimensions', [])
            metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                date_range_values = row.get('metrics', [])

                dims = []
                for header, dimension in zip(dimension_headers, dimensions):
                    dims.append(dimension)

                for i, values in enumerate(date_range_values):
                    for metricHeader, value in zip(metric_headers, values.get('values')):
                        final_dict[dates_range[8 - (int(dims[0]) + 2)]][dims[1]] = value
        return final_dict

    def week_report_by_hours(self):
        """Parses and reorganize the Analytics Reporting API V4 response.

        Args:
        response: An Analytics Reporting API V4 response reorganized.
        """
        analytics = self.initialize_analyticsreporting()
        response = self.get_report(
            analytics,
            ga_date_ranges=[{'startDate': '8daysAgo', 'endDate': 'yesterday'}],
            ga_metics=[{'expression': 'ga:sessions'}],
            ga_dimensions=[
                {'name': 'ga:hour'},
                {'name': 'ga:source'}
            ]
        )

        # get all metrics name
        source_metrics = []
        for row in response.get('reports', [])[0].get('data', {}).get('rows', []):
            if row["dimensions"][1] not in source_metrics:
                source_metrics.append(row["dimensions"][1])

        hours_range = []
        for i in range(0, 24):
            hours_range.append(i)

        final_dict = {}
        for d in hours_range:
            final_dict[d] = {}

        for x in final_dict:
            for y in source_metrics:
                final_dict[x][y] = 0

        for report in response.get('reports', []):
            column_header = report.get('columnHeader', {})
            dimension_headers = column_header.get('dimensions', [])
            metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                date_range_values = row.get('metrics', [])

                dims = []
                for header, dimension in zip(dimension_headers, dimensions):
                    dims.append(dimension)

                for i, values in enumerate(date_range_values):
                    for metricHeader, value in zip(metric_headers, values.get('values')):
                        final_dict[hours_range[24 - (int(dims[0]) + 1)]][dims[1]] = value
        return final_dict

    def test_connection(self):
        """Parses and prints the Analytics Reporting API V4 response.

        Args:
        response: An Analytics Reporting API V4 response.
        """
        analytics = self.initialize_analyticsreporting()
        return self.get_report(
            analytics,
            ga_date_ranges=[{'startDate': '8daysAgo', 'endDate': 'today'}],
            ga_metics=[{'expression': 'ga:sessions'}],
            ga_dimensions=[
                {'name': 'ga:nthDay'},
                {'name': 'ga:source'}
            ]
        )
